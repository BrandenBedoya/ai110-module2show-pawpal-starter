"""
main.py — PawPal+ CLI Demo
Verify backend logic here before touching the Streamlit UI.
Run with: python main.py
"""

from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", email="jordan@email.com")

mochi = Pet(name="Mochi", species="dog", age=3)
luna  = Pet(name="Luna",  species="cat", age=5)

owner.add_pet(mochi)
owner.add_pet(luna)

# --- Add tasks OUT OF ORDER intentionally to prove sorting works ---
mochi.add_task(Task("Evening walk",    time="18:30", frequency="daily",  pet_name="Mochi"))
mochi.add_task(Task("Flea medication", time="09:00", frequency="weekly", pet_name="Mochi"))
mochi.add_task(Task("Morning walk",    time="07:00", frequency="daily",  pet_name="Mochi"))

luna.add_task(Task("Grooming session", time="14:00", frequency="weekly", pet_name="Luna"))
luna.add_task(Task("Playtime",         time="19:00", frequency="none",   pet_name="Luna"))
luna.add_task(Task("Breakfast",        time="08:00", frequency="daily",  pet_name="Luna"))

scheduler = Scheduler(owner)

# --- 1. Sorted schedule ---
print("=" * 50)
print(f"  Today's Schedule for {owner.name}")
print("  (tasks added out of order — sorted by time)")
print("=" * 50)

for task in scheduler.sort_by_time():
    status_icon = "✓" if task.status == "complete" else "○"
    print(f"  {status_icon}  {task.time}  [{task.pet_name}]  {task.description}  ({task.frequency})")

# --- 2. Filter demo ---
print()
print("--- Filter: Mochi's tasks only ---")
for task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {task.time}  {task.description}")

print()
print("--- Filter: pending tasks only ---")
for task in scheduler.filter_tasks(status="pending"):
    print(f"  [{task.pet_name}]  {task.description}")

# --- 3. Conflict detection (deliberate conflict added) ---
print()
print("--- Conflict Check ---")
# Add a task at 09:00 for Mochi — same time as Flea medication
mochi.add_task(Task("Vet call", time="09:00", frequency="none", pet_name="Mochi"))
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts detected.")

# --- 4. Recurrence demo ---
print()
print("--- Recurrence Demo ---")
morning_walk = mochi.get_tasks()[2]  # Morning walk (index 2 after reorder)
print(f"  Completing: '{morning_walk.description}' (due {morning_walk.due_date})")
scheduler.mark_complete(morning_walk)
print(f"  Status is now: {morning_walk.status}")
print(f"  Next occurrence added for: {mochi.get_tasks()[-1].due_date}")

print()
print("Done.")
