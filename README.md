# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan daily care tasks across
one or more pets. It tracks each task's time, duration, priority, and recurrence,
then builds an explainable daily plan that fits the owner's available time — and
warns them when two tasks would collide.

## ✨ Features

Each feature below is backed by a real algorithm in
[pawpal_system.py](pawpal_system.py); the method that implements it is named so you
can jump straight to the code.

- **Urgency sorting** — orders tasks by a composite key (earliest due date →
  highest priority → shortest duration) so the most pressing care happens first.
  *(`Scheduler.sort_tasks`)*
- **Sorting by time of day** — orders tasks chronologically by clock time
  (`07:30 → 08:00 → 18:00`), independent of the calendar date. *(`Scheduler.sort_by_time`)*
- **Conflict warnings** — detects when two tasks are due at the same date **and**
  time, even across different pets, and returns human-readable warnings the UI
  surfaces as amber alerts. *(`Scheduler.detect_conflicts`)*
- **Daily / weekly recurrence** — completing a repeating task automatically
  schedules its next occurrence, using `timedelta` so month/year rollovers are
  correct (a daily task due Jan 31 becomes Feb 1). *(`Task.mark_complete`)*
- **Constraint-based daily planning** — greedily fits tasks into the owner's
  available minutes in urgency order, skipping anything that doesn't fit or is
  already done. *(`Scheduler.build_schedule`)*
- **Flexible filtering** — narrows tasks by pet, completion status, priority,
  due-by cutoff, and maximum duration. *(`Scheduler.filter_by`, `Scheduler.filter_tasks`)*
- **Task editing with validation** — updates only the fields you pass and rejects
  an invalid priority or a negative duration. *(`Task.edit_task`)*
- **Multi-pet management** — one owner can hold several pets, and the scheduler
  reasons over every pet's tasks together. *(`Owner.add_pet`, `Owner.view_tasks`)*
- **Professional Streamlit UI** — sorted task tables, green success summaries, and
  per-conflict warnings so the plan is easy to read and act on. *(`app.py`)*

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

```
Today's Schedule for Maya
========================================

 Daily plan for Rex (dog):
   07:30 - Morning walk (30 min) [priority: high]
   18:00 - Evening walk (30 min) [priority: high]

 Daily plan for Luna (cat):
   08:00 - Feed breakfast (10 min) [priority: medium]
   20:00 - Litter box cleaning (15 min) [priority: low]
```

## 🧪 Testing PawPal+

Run the full test suite from the project folder:

```bash
python -m pytest
```

Add `-v` for a per-test breakdown (`python -m pytest -v`).

The tests live in [test_pawpal.py](test_pawpal.py) and cover the core
scheduling behaviors:

- **Task completion** — `mark_complete()` flips a task's status to done.
- **Adding tasks** — `Pet.add_task()` attaches a task and updates the pet's count.
- **Urgency sorting** — `Scheduler.sort_tasks()` returns tasks in chronological
  (earliest due date first) order and leaves the caller's original list untouched.
- **Time-of-day sorting** — `Scheduler.sort_by_time()` orders tasks by clock
  time (07:30 → 12:00 → 18:00) regardless of calendar date.
- **Recurrence logic** — marking a `daily` task complete creates a new
  incomplete task for the following day (same time of day), attached to the same pet.
- **Conflict detection** — `Scheduler.detect_conflicts()` flags two tasks due
  at the same date *and time* (even across pets), does not flag tasks on the
  same day at different times, and does not flag tasks on different days.
- **Schedule building** — `Scheduler.build_schedule()` greedily fits tasks into
  the available time budget in urgency order and skips completed tasks.
- **Editing & validation** — `Task.edit_task()` updates only the fields passed
  and raises `ValueError` on an invalid priority or a negative duration.

Sample test output:

```
============================= test session starts =============================
collected 13 items

test_pawpal.py::test_mark_complete_changes_status PASSED                 [  7%]
test_pawpal.py::test_add_task_increases_pet_task_count PASSED            [ 15%]
test_pawpal.py::test_sort_tasks_returns_chronological_order PASSED       [ 23%]
test_pawpal.py::test_sort_by_time_orders_by_time_of_day PASSED           [ 30%]
test_pawpal.py::test_daily_task_recurrence_creates_next_day_task PASSED  [ 38%]
test_pawpal.py::test_detect_conflicts_flags_duplicate_times PASSED       [ 46%]
test_pawpal.py::test_detect_conflicts_same_day_different_time_is_not_a_conflict PASSED [ 53%]
test_pawpal.py::test_detect_conflicts_no_false_positive PASSED           [ 61%]
test_pawpal.py::test_build_schedule_fits_tasks_into_time_budget PASSED   [ 69%]
test_pawpal.py::test_build_schedule_skips_completed_tasks PASSED         [ 76%]
test_pawpal.py::test_edit_task_updates_fields PASSED                     [ 84%]
test_pawpal.py::test_edit_task_rejects_invalid_priority PASSED           [ 92%]
test_pawpal.py::test_edit_task_rejects_negative_duration PASSED          [100%]

============================== 13 passed in 0.05s ==============================
```

## 📐 Smarter Scheduling

The scheduling "brain" lives in the `Scheduler` service class in
[pawpal_system.py](pawpal_system.py), with recurrence handled on the `Task`
dataclass. Each feature below names the exact method that implements it.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_tasks()` | Chronological (time of day) and multi-key urgency ordering |
| Filtering | `Scheduler.filter_by()`, `Scheduler.filter_tasks()` | By pet, completion status, priority, due date, and duration |
| Conflict detection | `Scheduler.detect_conflicts()` | Flags tasks scheduled for the same date/time, even across pets |
| Recurring tasks | `Task.mark_complete()` | Auto-schedules the next `daily`/`weekly` occurrence |
| Constraint-based planning | `Scheduler.build_schedule()` | Ties it together: filter → sort → greedily fit into available time |

### Sorting behavior

Two complementary sorts are provided:

- **`Scheduler.sort_by_time()`** orders tasks by time of day, earliest first.
  Each task's `due_date` is a `datetime`, so the sort key is its time-of-day
  (`due_date.time()`) and clock times compare directly in the right order
  (`07:30 < 08:00 < 18:00`) regardless of the calendar date. Returns a new
  list, leaving the caller's original order untouched.
- **`Scheduler.sort_tasks()`** orders tasks by *urgency* using a composite key:
  earliest **due date** first, then highest **priority** (via the
  `PRIORITY_ORDER` map so `high < medium < low` rather than sorting
  alphabetically), then shortest **duration** so quick wins are knocked out
  sooner.

### Filtering behavior

- **`Scheduler.filter_by()`** filters by **pet** (`pet_name`) and/or
  **completion status** (`completed=True`/`False`/`None`). The two filters
  combine, e.g. "Rex's unfinished tasks."
- **`Scheduler.filter_tasks()`** is the broader planning filter: it drops
  completed tasks by default (`include_completed`) and additionally narrows by
  `priority`, a `due_by` cutoff, and `max_duration`. Any argument left as
  `None` is simply not applied.

### Conflict detection logic

**`Scheduler.detect_conflicts()`** groups the *incomplete* tasks by their due
date/time and reports any slot holding more than one task. Completed tasks are
excluded (a finished task can't clash), and detection works **across pets** —
two pets both due at 08:00 is still a conflict for the one owner who has to be
in two places at once. It never raises; it returns a list of human-readable
warning strings (an empty list means no clashes).

### Recurring task logic

**`Task.mark_complete()`** marks a task done and, if it repeats, schedules the
next occurrence. Frequency is one of `once`, `daily`, or `weekly`
(`FREQUENCIES`). For a recurring task it builds a fresh incomplete `Task` with
the same description/priority/duration and its due date advanced by the
matching `FREQUENCY_DELTA` `timedelta` — using `timedelta` means month/year
rollovers are handled correctly (a daily task due Jan 31 becomes Feb 1). The
new task is attached to the same pet and returned; a `once` task returns
`None` because there is nothing to reschedule.

## 📸 Demo Walkthrough

**What the UI lets you do:** set the owner name, add pets, add tasks (title,
duration, priority, due date + time), see a live task table sorted by urgency with
conflict warnings, and generate a time-boxed daily schedule.

**Example workflow:**

1. Add a pet - `Rex`, age 4, dog → *Add pet*.
2. Schedule tasks - add *Morning walk* (30 min, high, 07:30) and *Give
   medication* (5 min, high, 08:00).
3. Trigger a conflict - add a second pet Luna with *Feed breakfast* at 08:00;
   the table shows an amber warning that Rex's meds and Luna's breakfast collide.
4. View today's schedule - set available minutes to 60 and *Generate schedule*.

**Scheduler behaviors shown:** time-of-day sorting (`sort_by_time`), urgency sorting
(`sort_tasks`), cross-pet conflict warnings (`detect_conflicts`), daily/weekly
recurrence (`mark_complete`), and filtering to incomplete tasks (`filter_by`).

**Sample CLI output (`python main.py`):**

```text
Today's Schedule for Maya, sorted by time
=======================================================
   Wed 07/08 07:30 - Morning walk (30 min) [priority: high] [todo] [daily] (Rex)
   Wed 07/08 08:00 - Give medication (5 min) [priority: high] [todo] [daily] (Rex)
   Wed 07/08 08:00 - Feed breakfast (10 min) [priority: medium] [todo] [daily] (Luna)
   Wed 07/08 18:00 - Evening walk (30 min) [priority: high] [todo] [daily] (Rex)
   Wed 07/08 20:00 - Litter box cleaning (15 min) [priority: low] [todo] [weekly] (Luna)

Conflict check
=======================================================
   WARNING: 2 tasks overlap at Wed 07/08 08:00: Give medication (Rex), Feed breakfast (Luna)

Marking 'Morning walk' and 'Litter box cleaning' complete...
   -> daily task rescheduled to Thu 07/09
   -> weekly task rescheduled to Wed 07/15

Still to do (incomplete tasks only)
=======================================================
   Thu 07/09 07:30 - Morning walk (30 min) [priority: high] [todo] [daily] (Rex)
   Wed 07/08 08:00 - Give medication (5 min) [priority: high] [todo] [daily] (Rex)
   Wed 07/08 08:00 - Feed breakfast (10 min) [priority: medium] [todo] [daily] (Luna)
   Wed 07/08 18:00 - Evening walk (30 min) [priority: high] [todo] [daily] (Rex)
   Wed 07/15 20:00 - Litter box cleaning (15 min) [priority: low] [todo] [weekly] (Luna)
```
