"""
pawpal_system.py — PawPal+ Backend Logic
All four core classes live here. No UI logic belongs in this file.

Class hierarchy:
    Owner (has many) → Pet (has many) → Task
    Scheduler → talks to Owner to retrieve/manage tasks
"""

from dataclasses import dataclass, field
from datetime import date, timedelta


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
        """Append a Task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self.tasks


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
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Collect and return every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


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
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> list[Task]:
        """
        Return all tasks sorted chronologically by their 'time' field.
        Lexicographic sort works correctly for zero-padded HH:MM strings.
        """
        return sorted(self.get_all_tasks(), key=lambda task: task.time)

    def filter_tasks(self, status: str | None = None, pet_name: str | None = None) -> list[Task]:
        """
        Return tasks matching the given filter(s).
        Both status and pet_name filters can be combined.
        """
        tasks = self.get_all_tasks()
        if status:
            tasks = [t for t in tasks if t.status == status]
        if pet_name:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        return tasks

    def mark_complete(self, task: Task) -> None:
        """
        Mark a task complete. For recurring tasks, auto-create the next instance
        on the appropriate pet and add it to that pet's task list.
        """
        task.status = "complete"

        if task.frequency == "daily":
            next_due = task.due_date + timedelta(days=1)
        elif task.frequency == "weekly":
            next_due = task.due_date + timedelta(weeks=1)
        else:
            return  # non-recurring — nothing more to do

        next_task = Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            pet_name=task.pet_name,
            status="pending",
            due_date=next_due,
        )

        # Find the pet this task belongs to and add the next occurrence
        for pet in self.owner.pets:
            if pet.name == task.pet_name:
                pet.add_task(next_task)
                break

    def detect_conflicts(self) -> list[str]:
        """
        Flag any two tasks for the same pet scheduled at the exact same time.
        Returns a list of warning strings; never crashes.
        """
        warnings = []
        for pet in self.owner.pets:
            seen: dict[str, str] = {}  # time → description of first task seen
            for task in pet.get_tasks():
                if task.time in seen:
                    warnings.append(
                        f"Conflict for {pet.name}: '{seen[task.time]}' and "
                        f"'{task.description}' both scheduled at {task.time}"
                    )
                else:
                    seen[task.time] = task.description
        return warnings
