# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

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

## Features

- **Multi-pet support** — one owner profile manages any number of pets, each with their own task list
- **Task scheduling** — add care tasks with a description, time (HH:MM), and frequency (daily, weekly, or one-time)
- **Sorted daily view** — the schedule is always displayed in chronological order, regardless of the order tasks were added
- **Filter by pet or status** — narrow the schedule view to a specific pet or show only pending/completed tasks
- **Recurring tasks** — marking a daily or weekly task complete automatically schedules the next occurrence
- **Conflict detection** — the scheduler warns when two tasks for the same pet share the exact same time slot
- **Mark complete** — tasks can be marked done directly from the UI; recurring tasks self-schedule

## Smarter Scheduling

PawPal+ includes four algorithmic features in the `Scheduler` class:

- **Sort by time** — tasks are sorted chronologically using Python's `sorted()` with a lambda on the `HH:MM` string field. Zero-padded 24-hour strings sort correctly without any date parsing.
- **Filter tasks** — filter the task list by completion status (`pending`/`complete`), by pet name, or both combined.
- **Recurring tasks** — when `mark_complete()` is called on a `daily` or `weekly` task, a new instance is automatically created for the next due date using Python's `timedelta`.
- **Conflict detection** — the scheduler flags any two tasks for the same pet scheduled at the exact same time, returning a warning string rather than crashing.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The suite lives in `tests/test_pawpal.py` and covers five behaviors:

| Test | What it verifies |
|---|---|
| `test_task_completion` | `mark_complete()` flips task status from `pending` to `complete` |
| `test_task_addition` | Adding a task to a `Pet` increases its task count by 1 |
| `test_sort_correctness` | `sort_by_time()` returns tasks in ascending chronological order |
| `test_recurrence_logic` | Completing a `daily` task auto-creates a new task due the next day |
| `test_conflict_detection` | Two tasks for the same pet at the same time produce a warning |

**Confidence level: ★★★★☆ (4/5)**
All five tests pass. The main gap is duration-based conflict detection — the current scheduler only flags exact time matches, not overlapping windows. That would be the next thing to test and implement.

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
