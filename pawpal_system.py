"""PawPal system classes.

Generated from diagrams/uml_draft.mmd. Data-holding objects (Task, Pet,
Owner) use dataclasses to keep the code clean; Scheduler is a plain
service class since it only operates on tasks.
"""

from dataclasses import dataclass, field
from datetime import date

# Ordered priority levels so tasks can be ranked meaningfully (a bare string
# sorts alphabetically, which is not urgency order).
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    description: str
    due_date: date
    completion_status: bool = False
    priority: str = "medium"  # one of PRIORITY_ORDER
    duration: int = 0
    # Back-reference so a task flattened out of its pet still knows its owner.
    pet: "Pet | None" = field(default=None, repr=False)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completion_status = True

    def edit_task(
        self,
        *,
        description: str | None = None,
        due_date: date | None = None,
        priority: str | None = None,
        duration: int | None = None,
    ) -> None:
        """Update this task's details.

        Only the fields passed as keyword arguments are changed; everything
        else is left as-is. Priority is validated so a typo can't quietly
        break sorting later on.
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
