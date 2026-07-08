"""Simple tests for the PawPal system."""

from datetime import datetime, timedelta

import pytest

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip a task's status to done."""
    task = Task(description="Walk the dog", due_date=datetime(2026, 7, 8, 8, 0))

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

    task = Task(description="Feed Rex", due_date=datetime(2026, 7, 8, 8, 0))
    pet.add_task(task)

    # The task count should now be 1.
    assert len(pet.tasks) == 1


def test_sort_tasks_returns_chronological_order():
    """sort_tasks() should return tasks earliest-due-date first."""
    scheduler = Scheduler()

    # Build three tasks deliberately OUT of order (latest one first) so the
    # test actually proves the sort did something.
    later = Task(description="Vet visit", due_date=datetime(2026, 7, 10, 8, 0))
    earlier = Task(description="Morning walk", due_date=datetime(2026, 7, 8, 8, 0))
    middle = Task(description="Grooming", due_date=datetime(2026, 7, 9, 8, 0))
    unsorted = [later, earlier, middle]

    ordered = scheduler.sort_tasks(unsorted)

    # Pull the due dates back out and check they climb from earliest to latest.
    due_dates = [task.due_date for task in ordered]
    assert due_dates == [
        datetime(2026, 7, 8, 8, 0),
        datetime(2026, 7, 9, 8, 0),
        datetime(2026, 7, 10, 8, 0),
    ]

    # sort_tasks returns a NEW list; the original should be untouched.
    assert unsorted == [later, earlier, middle]


def test_sort_by_time_orders_by_time_of_day():
    """sort_by_time() should order by clock time, ignoring the calendar date."""
    scheduler = Scheduler()

    # Same day, entered out of time order. Before the datetime fix this always
    # collapsed to "00:00" and never reordered -- this test guards that bug.
    evening = Task(description="Evening walk", due_date=datetime(2026, 7, 8, 18, 0))
    morning = Task(description="Morning walk", due_date=datetime(2026, 7, 8, 7, 30))
    noon = Task(description="Lunch", due_date=datetime(2026, 7, 8, 12, 0))

    ordered = scheduler.sort_by_time([evening, morning, noon])

    assert [t.description for t in ordered] == ["Morning walk", "Lunch", "Evening walk"]


def test_daily_task_recurrence_creates_next_day_task():
    """Completing a 'daily' task should spawn a fresh task for the next day."""
    pet = Pet(name="Rex", age=3, species="dog")
    task = Task(
        description="Morning walk",
        due_date=datetime(2026, 7, 8, 7, 30),
        frequency="daily",
    )
    pet.add_task(task)

    next_task = task.mark_complete()

    # The original is now done...
    assert task.completion_status is True
    # ...and a brand-new task was returned for the FOLLOWING day, same time.
    assert next_task is not None
    assert next_task.due_date == datetime(2026, 7, 8, 7, 30) + timedelta(days=1)
    assert next_task.due_date == datetime(2026, 7, 9, 7, 30)
    # The new one starts incomplete and is attached to the same pet.
    assert next_task.completion_status is False
    assert next_task in pet.tasks
    # Pet now has the original completed task plus the new one.
    assert len(pet.tasks) == 2


def test_detect_conflicts_flags_duplicate_times():
    """Two incomplete tasks due at the same date/time should be flagged."""
    scheduler = Scheduler()
    rex = Pet(name="Rex", age=3, species="dog")
    milo = Pet(name="Milo", age=2, species="cat")

    # Both pets need attention at the exact same time -> a scheduling clash.
    clash_time = datetime(2026, 7, 8, 8, 0)
    rex.add_task(Task(description="Walk Rex", due_date=clash_time))
    milo.add_task(Task(description="Feed Milo", due_date=clash_time))

    warnings = scheduler.detect_conflicts(rex.tasks + milo.tasks)

    # Exactly one clash should be reported, mentioning both pets.
    assert len(warnings) == 1
    assert "Rex" in warnings[0]
    assert "Milo" in warnings[0]


def test_detect_conflicts_same_day_different_time_is_not_a_conflict():
    """Two tasks on the same DAY but different TIMES should not clash."""
    scheduler = Scheduler()
    pet = Pet(name="Rex", age=3, species="dog")
    pet.add_task(Task(description="Morning walk", due_date=datetime(2026, 7, 8, 7, 30)))
    pet.add_task(Task(description="Evening walk", due_date=datetime(2026, 7, 8, 18, 0)))

    # This is the case the old date-only code got wrong (it flagged them).
    assert scheduler.detect_conflicts(pet.tasks) == []


def test_detect_conflicts_no_false_positive():
    """Tasks on different days should NOT be flagged as conflicts."""
    scheduler = Scheduler()
    pet = Pet(name="Rex", age=3, species="dog")
    pet.add_task(Task(description="Walk", due_date=datetime(2026, 7, 8, 8, 0)))
    pet.add_task(Task(description="Vet", due_date=datetime(2026, 7, 9, 8, 0)))

    assert scheduler.detect_conflicts(pet.tasks) == []


def test_build_schedule_fits_tasks_into_time_budget():
    """build_schedule() should pick, in urgency order, tasks that fit the budget."""
    scheduler = Scheduler()
    owner = Owner(name="Maya")
    pet = Pet(name="Rex", age=3, species="dog")
    owner.add_pet(pet)

    # Three tasks, same day, all high priority so DURATION is the tie-breaker
    # (shortest first). Total is 70 min; we only give the planner 60.
    pet.add_task(
        Task(description="Walk", due_date=datetime(2026, 7, 8, 8, 0),
             duration=30, priority="high")
    )
    pet.add_task(
        Task(description="Feed", due_date=datetime(2026, 7, 8, 8, 0),
             duration=10, priority="high")
    )
    pet.add_task(
        Task(description="Groom", due_date=datetime(2026, 7, 8, 8, 0),
             duration=30, priority="high")
    )

    plan = scheduler.build_schedule(owner, available_minutes=60)

    # Shortest-first ordering (10, 30, 30) means all three would be 70 min, so
    # the last 30-min task is dropped; 10 + 30 = 40 <= 60 fits.
    descriptions = [t.description for t in plan]
    assert descriptions == ["Feed", "Walk"]
    assert sum(t.duration for t in plan) <= 60


def test_build_schedule_skips_completed_tasks():
    """Completed tasks should never appear in a generated plan."""
    scheduler = Scheduler()
    owner = Owner(name="Maya")
    pet = Pet(name="Rex", age=3, species="dog")
    owner.add_pet(pet)

    done = Task(description="Old walk", due_date=datetime(2026, 7, 8, 8, 0), duration=10)
    done.mark_complete()  # a "once" task -> just marks it done
    pet.add_task(done)
    pet.add_task(Task(description="New walk", due_date=datetime(2026, 7, 8, 9, 0), duration=10))

    plan = scheduler.build_schedule(owner, available_minutes=60)

    assert [t.description for t in plan] == ["New walk"]


def test_edit_task_updates_fields():
    """edit_task() should change only the fields that are passed."""
    task = Task(description="Walk", due_date=datetime(2026, 7, 8, 8, 0), priority="low")

    task.edit_task(priority="high", duration=25)

    assert task.priority == "high"
    assert task.duration == 25
    # Untouched fields keep their original values.
    assert task.description == "Walk"


def test_edit_task_rejects_invalid_priority():
    """An unknown priority should raise ValueError and leave the task unchanged."""
    task = Task(description="Walk", due_date=datetime(2026, 7, 8, 8, 0), priority="low")

    with pytest.raises(ValueError):
        task.edit_task(priority="urgent")

    # The bad edit must not have partially applied.
    assert task.priority == "low"


def test_edit_task_rejects_negative_duration():
    """A negative duration should raise ValueError."""
    task = Task(description="Walk", due_date=datetime(2026, 7, 8, 8, 0), duration=10)

    with pytest.raises(ValueError):
        task.edit_task(duration=-5)

    assert task.duration == 10
