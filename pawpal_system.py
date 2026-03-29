"""
pawpal_system.py — PawPal+ Backend Logic
All four core classes live here. No UI logic belongs in this file.

Class hierarchy:
    Owner (has many) → Pet (has many) → Task
    Scheduler → talks to Owner to retrieve/manage tasks
"""

from dataclasses import dataclass, field
from datetime import date


# ---------------------------------------------------------------------------
# Task — atomic unit of pet care (dataclass for clean attribute declaration)
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """A single care activity assigned to a pet."""
    description: str        # e.g. "Morning walk"
    time: str               # "HH:MM" 24-hour format, used for sorting
    frequency: str          # "daily", "weekly", or "none"
    pet_name: str           # which pet this task belongs to
    status: str = "pending" # "pending" or "complete"
    due_date: date = field(default_factory=date.today)


# ---------------------------------------------------------------------------
# Pet — holds pet info + its list of Tasks (dataclass)
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    """Represents a pet with its own list of care tasks."""
    name: str
    species: str            # e.g. "dog", "cat", "rabbit"
    age: int                # years
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a Task to this pet's task list."""
        pass

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        pass


# ---------------------------------------------------------------------------
# Owner — root of the data tree; holds pets (regular class for behavior)
# ---------------------------------------------------------------------------

class Owner:
    """Represents a pet owner who manages one or more pets."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Collect and return every task across all pets."""
        pass


# ---------------------------------------------------------------------------
# Scheduler — algorithmic brain; sorts, filters, detects conflicts, recurs
# ---------------------------------------------------------------------------

class Scheduler:
    """
    Manages task retrieval and scheduling logic for an Owner.
    Does NOT own data — it reads from Owner and writes back via Task mutations.
    """

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        """Retrieve every task across all of the owner's pets."""
        pass

    def sort_by_time(self) -> list[Task]:
        """
        Return all tasks sorted chronologically by their 'time' field.
        Uses sorted() with a lambda on the 'HH:MM' string — lexicographic
        sort works correctly for zero-padded 24-hour time strings.
        """
        pass

    def filter_tasks(self, status: str = None, pet_name: str = None) -> list[Task]:
        """
        Return tasks matching the given filter(s).
        - status: filter by 'pending' or 'complete'
        - pet_name: filter to a specific pet
        Both filters can be combined.
        """
        pass

    def mark_complete(self, task: Task) -> None:
        """
        Mark a task complete. For recurring tasks, auto-create the next instance:
        - 'daily'  → new task with due_date + timedelta(days=1)
        - 'weekly' → new task with due_date + timedelta(weeks=1)
        """
        pass

    def detect_conflicts(self) -> list[str]:
        """
        Check for scheduling conflicts: two tasks for the same pet at the same time.
        Returns a list of warning strings (never crashes).
        Returns an empty list if no conflicts are found.
        """
        pass
