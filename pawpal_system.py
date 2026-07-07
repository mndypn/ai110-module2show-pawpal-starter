"""PawPal system class skeleton.

Generated from diagrams/uml_draft.mmd. Data-holding objects (Task, Pet,
Owner) use dataclasses to keep the code clean; Scheduler is a plain
service class since it only operates on tasks.
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    description: str
    due_date: date
    completion_status: bool = False
    priority: str = ""
    duration: int = 0

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        ...

    def edit_task(self) -> None:
        """Update this task's details."""
        ...


@dataclass
class Pet:
    name: str
    age: int
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        ...


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        ...

    def view_tasks(self) -> list[Task]:
        """Return all tasks across this owner's pets."""
        ...


class Scheduler:
    def filter_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return a filtered subset of the given tasks."""
        ...

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return the given tasks in sorted order."""
        ...
