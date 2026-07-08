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

    # 2. Add tasks with different times of day.
    rex.add_task(Task(description="Morning walk", due_date=at(7, 30),
                       priority="high", duration=30))
    luna.add_task(Task(description="Feed breakfast", due_date=at(8, 0),
                       priority="medium", duration=10))
    rex.add_task(Task(description="Evening walk", due_date=at(18, 0),
                      priority="high", duration=30))
    luna.add_task(Task(description="Litter box cleaning", due_date=at(20, 0),
                       priority="low", duration=15))

    # 3. Build and print today's schedule, grouped by pet and ordered by urgency.
    scheduler = Scheduler()

    print(f"Today's Schedule for {owner.name}")
    print("=" * 40)
    for pet in owner.pets:
        print(f"\n Daily plan for {pet.name} ({pet.species}):")
        for task in scheduler.sort_tasks(pet.tasks):
            time_str = task.due_date.strftime("%H:%M")
            print(f"   {time_str} - {task.description} "
                  f"({task.duration} min) [priority: {task.priority}]")


if __name__ == "__main__":
    main()
