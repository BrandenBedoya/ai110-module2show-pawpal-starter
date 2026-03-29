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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
