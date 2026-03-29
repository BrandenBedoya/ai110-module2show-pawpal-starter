"""
tests/test_pawpal.py — Automated test suite for PawPal+ backend logic.
Run with: python -m pytest
"""

import pytest
from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


# ---------------------------------------------------------------------------
# Shared fixtures — reusable setup across tests
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_owner():
    """An Owner with two pets and a handful of tasks."""
    owner = Owner(name="Jordan", email="jordan@email.com")

    mochi = Pet(name="Mochi", species="dog", age=3)
    luna  = Pet(name="Luna",  species="cat", age=5)

    mochi.add_task(Task("Morning walk",    time="07:00", frequency="daily",  pet_name="Mochi"))
    mochi.add_task(Task("Evening walk",    time="18:30", frequency="daily",  pet_name="Mochi"))
    mochi.add_task(Task("Flea medication", time="09:00", frequency="weekly", pet_name="Mochi"))

    luna.add_task(Task("Breakfast",        time="08:00", frequency="daily",  pet_name="Luna"))
    luna.add_task(Task("Grooming session", time="14:00", frequency="weekly", pet_name="Luna"))

    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner


# ---------------------------------------------------------------------------
# Test 1: mark_complete() changes task status to "complete"
# ---------------------------------------------------------------------------

def test_task_completion(sample_owner):
    """mark_complete() should flip status from 'pending' to 'complete'."""
    scheduler = Scheduler(sample_owner)
    task = sample_owner.pets[0].get_tasks()[0]  # Mochi's morning walk

    assert task.status == "pending"
    scheduler.mark_complete(task)
    assert task.status == "complete"


# ---------------------------------------------------------------------------
# Test 2: add_task() increases the pet's task count
# ---------------------------------------------------------------------------

def test_task_addition(sample_owner):
    """Adding a task to a pet should increase that pet's task count by 1."""
    mochi = sample_owner.pets[0]
    before = len(mochi.get_tasks())

    new_task = Task("Vet appointment", time="11:00", frequency="none", pet_name="Mochi")
    mochi.add_task(new_task)

    assert len(mochi.get_tasks()) == before + 1


# ---------------------------------------------------------------------------
# Test 3: sort_by_time() returns tasks in chronological order
# ---------------------------------------------------------------------------

def test_sort_correctness(sample_owner):
    """Tasks returned by sort_by_time() should be in ascending HH:MM order."""
    scheduler = Scheduler(sample_owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


# ---------------------------------------------------------------------------
# Test 4: completing a daily task auto-creates a next-day task
# ---------------------------------------------------------------------------

def test_recurrence_logic(sample_owner):
    """Completing a 'daily' task should add a new task due the next day."""
    mochi = sample_owner.pets[0]
    scheduler = Scheduler(sample_owner)

    daily_task = mochi.get_tasks()[0]  # Morning walk — daily
    original_due = daily_task.due_date
    task_count_before = len(mochi.get_tasks())

    scheduler.mark_complete(daily_task)

    assert len(mochi.get_tasks()) == task_count_before + 1
    next_task = mochi.get_tasks()[-1]
    assert next_task.due_date == original_due + timedelta(days=1)
    assert next_task.status == "pending"


# ---------------------------------------------------------------------------
# Test 5: detect_conflicts() flags tasks at the same time for the same pet
# ---------------------------------------------------------------------------

def test_conflict_detection(sample_owner):
    """Two tasks for the same pet at the same time should produce a warning."""
    mochi = sample_owner.pets[0]
    # Add a task that collides with "Morning walk" at 07:00
    mochi.add_task(Task("Breakfast", time="07:00", frequency="none", pet_name="Mochi"))

    scheduler = Scheduler(sample_owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) > 0
    assert any("07:00" in warning for warning in conflicts)
