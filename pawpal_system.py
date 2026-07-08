"""PawPal system class skeleton.

Generated from diagrams/uml_draft.mmd. Data-holding objects (Task, Pet,
Owner) use dataclasses to keep the code clean; Scheduler is a plain
service class since it only operates on tasks.
"""

from collections.abc import Callable
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
