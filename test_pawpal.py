"""Simple tests for the PawPal system."""

from datetime import date

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip a task's status to done."""
    task = Task(description="Walk the dog", due_date=date(2026, 7, 8))

    # A new task starts out incomplete.
    assert task.completion_status is False

    task.mark_complete()

    # After marking complete, the status should be True.
    assert task.completion_status is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count."""
    pet = Pet(name="Rex", age=3, species="dog")

    # A new pet has no tasks yet.
    assert len(pet.tasks) == 0

    task = Task(description="Feed Rex", due_date=date(2026, 7, 8))
    pet.add_task(task)

    # The task count should now be 1.
    assert len(pet.tasks) == 1
