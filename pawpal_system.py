"""PawPal system classes.

Generated from diagrams/uml_draft.mmd. Data-holding objects (Task, Pet,
Owner) use dataclasses to keep the code clean; Scheduler is a plain
service class since it only operates on tasks.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta

# Ordered priority levels so tasks can be ranked meaningfully (a bare string
# sorts alphabetically, which is not urgency order).
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# How often a task repeats. "once" tasks never come back after completion;
# "daily"/"weekly" tasks auto-schedule their next occurrence. Using timedelta
# (instead of naively adding to the day number) handles month and year
# rollovers correctly -- e.g. a daily task on Jan 31 becomes Feb 1.
FREQUENCY_DELTA = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}
FREQUENCIES = {"once"} | set(FREQUENCY_DELTA)


@dataclass
class Task:
    description: str
    due_date: date
    completion_status: bool = False
    priority: str = "medium"  # one of PRIORITY_ORDER
    duration: int = 0
    frequency: str = "once"  # one of FREQUENCIES
    # Back-reference so a task flattened out of its pet still knows its owner.
    pet: "Pet | None" = field(default=None, repr=False)

    def mark_complete(self) -> "Task | None":
        """Mark this task done and, if it repeats, schedule the next one.

        For a "daily" or "weekly" task we build a fresh Task for the next
        occurrence -- same description/priority/duration, but with its due
        date advanced by the matching timedelta -- and attach it to the same
        pet. The new task starts incomplete. Returns the newly created task,
        or None for a one-off ("once") task that has nothing to repeat.
        """
        self.completion_status = True

        delta = FREQUENCY_DELTA.get(self.frequency)
        if delta is None:
            return None  # one-off task: nothing to reschedule

        next_task = Task(
            description=self.description,
            due_date=self.due_date + delta,
            priority=self.priority,
            duration=self.duration,
            frequency=self.frequency,
        )
        if self.pet is not None:
            self.pet.add_task(next_task)
        return next_task

    def edit_task(
        self,
        *,
        description: str | None = None,
        due_date: date | None = None,
        priority: str | None = None,
        duration: int | None = None,
        frequency: str | None = None,
    ) -> None:
        """Update this task's details.

        Only the fields passed as keyword arguments are changed; everything
        else is left as-is. Priority and frequency are validated so a typo
        can't quietly break sorting or recurrence later on.
        """
        if description is not None:
            self.description = description
        if due_date is not None:
            self.due_date = due_date
        if priority is not None:
            if priority not in PRIORITY_ORDER:
                raise ValueError(
                    f"priority must be one of {sorted(PRIORITY_ORDER)}, got {priority!r}"
                )
            self.priority = priority
        if duration is not None:
            if duration < 0:
                raise ValueError("duration cannot be negative")
            self.duration = duration
        if frequency is not None:
            if frequency not in FREQUENCIES:
                raise ValueError(
                    f"frequency must be one of {sorted(FREQUENCIES)}, got {frequency!r}"
                )
            self.frequency = frequency


@dataclass
class Pet:
    name: str
    age: int
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet and set its back-reference."""
        task.pet = self
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def view_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets (flattened)."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The 'brain': retrieves, organizes, and manages tasks across pets."""

    def filter_tasks(
        self,
        tasks: list[Task],
        *,
        include_completed: bool = False,
        priority: str | None = None,
        due_by: date | None = None,
        max_duration: int | None = None,
    ) -> list[Task]:
        """Return the subset of tasks matching the given constraints.

        By default completed tasks are dropped (you rarely want to re-plan
        something that's already done). Any other argument left as None is
        simply not applied as a filter.
        """
        result = []
        for task in tasks:
            if not include_completed and task.completion_status:
                continue
            if priority is not None and task.priority != priority:
                continue
            if due_by is not None and task.due_date > due_by:
                continue
            if max_duration is not None and task.duration > max_duration:
                continue
            result.append(task)
        return result

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Find tasks that are scheduled for the exact same date and time.

        Lightweight strategy: group the (incomplete) tasks by their due date
        and time, then report any group with more than one task. This never
        raises -- it just returns a list of human-readable warning strings so
        the caller can print them and keep running. An empty list means no
        clashes were found.

        Works across pets: two pets both due at 08:00 is still a conflict for
        the one owner who has to be in two places at once.
        """
        by_time: defaultdict[date, list[Task]] = defaultdict(list)
        for task in tasks:
            if not task.completion_status:  # a finished task can't clash
                by_time[task.due_date].append(task)

        warnings = []
        for when, clashing in by_time.items():
            if len(clashing) <= 1:
                continue  # only one task at this time -- no conflict
            when_str = when.strftime("%a %m/%d %H:%M")
            names = ", ".join(
                f"{t.description} ({t.pet.name if t.pet else '?'})"
                for t in clashing
            )
            warnings.append(f"WARNING: {len(clashing)} tasks overlap at {when_str}: {names}")
        return warnings

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by time of day, earliest first.

        The sort key is each task's due time formatted as an "HH:MM" string
        (e.g. "07:30"). Because the hour and minute are zero-padded to two
        digits, a plain string comparison already gives the correct
        chronological order -- "07:30" < "08:00" < "18:00" -- so the lambda
        just hands that string to sorted() as the key. Returns a new list so
        the caller's original order is left untouched.
        """
        return sorted(tasks, key=lambda t: t.due_date.strftime("%H:%M"))

    def filter_by(
        self,
        tasks: list[Task],
        *,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return the tasks matching an optional completion status / pet name.

        - completed=True keeps only finished tasks, completed=False keeps only
          unfinished ones, and completed=None (the default) ignores status.
        - pet_name keeps only tasks belonging to that pet; None ignores it.

        Both filters can be combined, e.g. "Rex's unfinished tasks".
        """
        result = []
        for task in tasks:
            if completed is not None and task.completion_status != completed:
                continue
            if pet_name is not None and (task.pet is None or task.pet.name != pet_name):
                continue
            result.append(task)
        return result

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return the tasks ordered by urgency.

        Sort key: earliest due date first, then highest priority, then
        shortest duration (a quick task can be knocked out sooner). Returns a
        new list so the caller's original order is preserved.
        """
        return sorted(
            tasks,
            key=lambda t: (
                t.due_date,
                PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)),
                t.duration,
            ),
        )

    def build_schedule(
        self,
        owner: Owner,
        *,
        available_minutes: int | None = None,
        due_by: date | None = None,
    ) -> list[Task]:
        """Retrieve every task for an owner and organize it into a plan.

        Pulls the owner's tasks, filters out completed (and anything past the
        `due_by` cutoff), sorts by urgency, then greedily fits tasks into the
        available time budget. Tasks that don't fit are left off the plan.
        """
        tasks = self.filter_tasks(owner.view_tasks(), due_by=due_by)
        ordered = self.sort_tasks(tasks)

        if available_minutes is None:
            return ordered

        plan = []
        remaining = available_minutes
        for task in ordered:
            if task.duration <= remaining:
                plan.append(task)
                remaining -= task.duration
        return plan
