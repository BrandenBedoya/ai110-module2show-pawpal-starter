# PawPal+ Project Reflection

## 1. System Design

**Three core user actions (Step 1):**

1. Add a pet to an owner's profile (name, species, age)
2. Add a care task to a specific pet (description, scheduled time, frequency)
3. View a sorted daily schedule across all pets, with conflict warnings highlighted

**a. Initial design**

The system uses four classes organized in a clear ownership hierarchy:

- **Task** (dataclass): The atomic unit of care. Holds what needs to happen (`description`), when (`time` in HH:MM), how often (`frequency`: daily/weekly/none), which pet it belongs to (`pet_name`), its current `status`, and its `due_date`. Using a dataclass keeps attribute declaration clean and avoids boilerplate `__init__` code.

- **Pet** (dataclass): Represents a single animal with basic info (`name`, `species`, `age`) and a list of its `Task` objects. Exposes `add_task()` and `get_tasks()`. Using a dataclass here is valid because a Pet's primary job is holding data — its behavior is minimal.

- **Owner** (regular class): The root of the data tree. Holds the owner's `name`, `email`, and a list of `Pet` objects. Uses a regular class because it has meaningful behavior (`add_pet`, `get_all_tasks`) that benefits from explicit `__init__` control and potential future extension.

- **Scheduler** (regular class): The algorithmic brain. It holds a reference to an `Owner` and exposes all scheduling operations: `sort_by_time()`, `filter_tasks()`, `mark_complete()` (with recurrence logic), and `detect_conflicts()`. It does not own any data — it reads from Owner and mutates Tasks in place.

Key relationship: `Owner → Pet → Task` is a strict composition chain. `Scheduler` sits outside this chain and manages it.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, simply used Claude to help refactor and make sure the relationships made sense between pets, owners, and tasks

--

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two constraints: **time** (HH:MM) and **completion status** (pending/complete). Time was prioritized first because the core user need is knowing *when* to do something. Status was second because filtering completed tasks reduces noise in the daily view. Pet name filtering was added so owners with multiple pets can focus on one animal at a time.

**b. Tradeoffs**

The conflict detector only flags tasks scheduled at the **exact same time** — it does not check for overlapping durations. For example, a 30-minute walk starting at 07:00 and a 15-minute feeding starting at 07:20 would not be flagged as a conflict, even though they overlap in reality.

This is a reasonable tradeoff for this scenario because tasks in PawPal+ don't currently have a duration field — adding one would increase complexity significantly for a v1 app. Exact-time matching catches the most common mistake (accidentally double-booking a slot) without requiring the scheduler to reason about time ranges.

---

## 3. AI Collaboration

**a. How you used AI**

Claude Code (via the VS Code extension) was the primary AI tool used throughout this project. It was most effective in three ways:

1. **System design** — used in Phase 1 to brainstorm the four-class architecture, generate the Mermaid UML, and translate it into class skeletons with correct Python dataclass syntax.
2. **Implementation scaffolding** — in Phase 2, used to flesh out all method bodies in `pawpal_system.py`, particularly the `mark_complete()` recurrence logic using `timedelta` and the `detect_conflicts()` dictionary-based approach.
3. **Debugging and type checking** — Pylance (enabled in Phase 1) caught a type mismatch in `filter_tasks()` where `str` was declared but `None` was being passed. AI helped explain the fix (`str | None` union type) and why it matters.

The most effective prompt style was giving specific context: referencing the file, describing the exact behavior needed, and asking for reasoning alongside the code — not just the answer.

**b. Judgment and verification**

During Phase 4, Claude initially structured `detect_conflicts()` to check conflicts across *all pets* together rather than per pet. This would have incorrectly flagged two different pets having tasks at the same time as a conflict — which isn't actually a problem. The fix was to scope the conflict check *per pet* using a separate `seen` dictionary inside the loop for each pet. The logic was verified by writing `test_conflict_detection` which deliberately adds a collision on one pet and checks that only that conflict appears, not false positives from other pets.

---

## 4. Testing and Verification

**a. What you tested**

Five behaviors were tested in `tests/test_pawpal.py`:

- **Task completion** — `mark_complete()` mutates status correctly
- **Task addition** — `Pet.add_task()` grows the task list
- **Sort correctness** — `sort_by_time()` returns tasks in ascending HH:MM order regardless of insertion order
- **Recurrence logic** — completing a `daily` task adds a new task with `due_date + 1 day`
- **Conflict detection** — same-time tasks on the same pet produce a warning string

These were important because they cover the three core algorithmic behaviors (sort, recur, conflict) plus the two most basic data mutations (add, complete). If any of these break, the app's core value is broken.

**b. Confidence**

**4/5 stars.** All five tests pass and cover the primary happy paths. The gap is duration-based conflict detection — the scheduler only catches exact time collisions, not overlapping windows (e.g., a 30-min task at 07:00 overlapping a task at 07:20). That would require adding a `duration` field to `Task` and more complex interval logic, which is a natural next iteration.

---

## 5. Reflection

**a. What went well**

The CLI-first workflow was the most valuable structural decision. By verifying all logic in `main.py` before touching `app.py`, bugs in the backend were caught early — before the UI added a second layer of complexity. The `Scheduler` class staying separate from the data hierarchy (`Owner → Pet → Task`) also kept the code clean: adding a new algorithm only required touching one class.

**b. What you would improve**

The `Task` class doesn't have a `duration` field, which limits conflict detection to exact-time matching. A future iteration would add `duration_minutes: int` to `Task` and update `detect_conflicts()` to check for time-window overlaps. The UI would also benefit from an edit/delete task feature — right now tasks can only be added, not removed.

**c. Key takeaway**

The most important lesson was that AI is a powerful *executor* but needs a human *architect*. When given a clear design (the UML, the class relationships, the specific method behaviors), Claude produced correct, clean code quickly. When the design was ambiguous, the AI made reasonable but wrong assumptions (like the cross-pet conflict bug). The lead architect role — defining constraints, reviewing output, and catching edge cases — was always the human's job.
