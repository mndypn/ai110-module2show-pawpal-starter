"""PawPal demo: build a small household of pets and print today's schedule."""

from datetime import datetime

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    # Anchor every task to today so they all show up on "Today's Schedule".
    today = datetime.now()

    def at(hour: int, minute: int = 0) -> datetime:
        """A datetime at today's date but a specific time of day."""
        return today.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # 1. Create an owner and two pets.
    owner = Owner(name="Maya")
    rex = Pet(name="Rex", age=4, species="dog")
    luna = Pet(name="Luna", age=2, species="cat")
    owner.add_pet(rex)
    owner.add_pet(luna)

    # 2. Add tasks *out of order* on purpose, so we can prove the sorting
    #    method is really doing the work (and not just echoing insert order).
    #    Walks and feeding repeat every day; the vet visit is a one-off.
    rex.add_task(Task(description="Evening walk", due_date=at(18, 0),
                      priority="high", duration=30, frequency="daily"))
    luna.add_task(Task(description="Litter box cleaning", due_date=at(20, 0),
                       priority="low", duration=15, frequency="weekly"))
    rex.add_task(Task(description="Morning walk", due_date=at(7, 30),
                      priority="high", duration=30, frequency="daily"))
    luna.add_task(Task(description="Feed breakfast", due_date=at(8, 0),
                       priority="medium", duration=10, frequency="daily"))
    # Deliberate clash: Rex's meds land at 08:00, same as Luna's breakfast.
    rex.add_task(Task(description="Give medication", due_date=at(8, 0),
                      priority="high", duration=5, frequency="daily"))

    scheduler = Scheduler()

    def show(task: Task) -> None:
        date_str = task.due_date.strftime("%a %m/%d %H:%M")
        status = "done" if task.completion_status else "todo"
        pet_name = task.pet.name if task.pet else "?"
        print(f"   {date_str} - {task.description} "
              f"({task.duration} min) [priority: {task.priority}] "
              f"[{status}] [{task.frequency}] ({pet_name})")

    # 3. Sort every task by time of day using the new sort_by_time().
    print(f"Today's Schedule for {owner.name}, sorted by time")
    print("=" * 55)
    for task in scheduler.sort_by_time(owner.view_tasks()):
        show(task)

    # 3b. Check for scheduling clashes. detect_conflicts() returns warning
    #     strings instead of raising, so the program keeps running.
    print("\nConflict check")
    print("=" * 55)
    conflicts = scheduler.detect_conflicts(owner.view_tasks())
    if conflicts:
        for warning in conflicts:
            print(f"   {warning}")
    else:
        print("   No conflicts found.")

    # 4. Complete the two morning tasks. Because they're recurring, each one
    #    automatically spawns its next occurrence for tomorrow / next week.
    print("\nMarking 'Morning walk' and 'Litter box cleaning' complete...")
    for pet in owner.pets:
        for task in list(pet.tasks):  # snapshot: mark_complete appends new tasks
            if task.description in {"Morning walk", "Litter box cleaning"}:
                new_task = task.mark_complete()
                if new_task is not None:
                    when = new_task.due_date.strftime("%a %m/%d")
                    print(f"   -> {new_task.frequency} task rescheduled to {when}")

    # 5. The full list now includes the freshly created future occurrences.
    print("\nSchedule after completing recurring tasks")
    print("=" * 55)
    for task in scheduler.sort_by_time(owner.view_tasks()):
        show(task)

    # 6. Filter: only unfinished tasks (the completed originals drop out,
    #    their new occurrences remain).
    print("\nStill to do (incomplete tasks only)")
    print("=" * 55)
    todo = scheduler.filter_by(owner.view_tasks(), completed=False)
    for task in scheduler.sort_by_time(todo):
        show(task)


if __name__ == "__main__":
    main()
