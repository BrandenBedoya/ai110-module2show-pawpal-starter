"""
app.py — PawPal+ Streamlit UI
Imports all logic from pawpal_system.py. No scheduling logic lives here.
"""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Session state — persists Owner object across Streamlit rerenders
# ---------------------------------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = None

# ---------------------------------------------------------------------------
# Section 1: Owner setup
# ---------------------------------------------------------------------------

st.header("Owner Setup")

if st.session_state.owner is None:
    with st.form("owner_form"):
        owner_name  = st.text_input("Your name",  value="Jordan")
        owner_email = st.text_input("Your email", value="jordan@email.com")
        submitted   = st.form_submit_button("Create profile")

    if submitted:
        st.session_state.owner = Owner(name=owner_name, email=owner_email)
        st.rerun()
else:
    owner: Owner = st.session_state.owner
    st.success(f"Welcome back, {owner.name}!")

    # -----------------------------------------------------------------------
    # Section 2: Add a pet
    # -----------------------------------------------------------------------

    st.header("Add a Pet")
    with st.form("pet_form"):
        pet_name    = st.text_input("Pet name", value="Mochi")
        pet_species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])
        pet_age     = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
        add_pet_btn = st.form_submit_button("Add pet")

    if add_pet_btn:
        new_pet = Pet(name=pet_name, species=pet_species, age=int(pet_age))
        owner.add_pet(new_pet)
        st.success(f"{pet_name} added!")

    # -----------------------------------------------------------------------
    # Section 3: Add a task
    # -----------------------------------------------------------------------

    st.header("Add a Task")
    if not owner.pets:
        st.info("Add a pet first before scheduling tasks.")
    else:
        pet_names = [p.name for p in owner.pets]
        with st.form("task_form"):
            target_pet   = st.selectbox("Assign to pet", pet_names)
            task_desc    = st.text_input("Task description", value="Morning walk")
            task_time    = st.text_input("Time (HH:MM)", value="07:00")
            task_freq    = st.selectbox("Frequency", ["daily", "weekly", "none"])
            add_task_btn = st.form_submit_button("Add task")

        if add_task_btn:
            new_task = Task(
                description=task_desc,
                time=task_time,
                frequency=task_freq,
                pet_name=target_pet,
            )
            for pet in owner.pets:
                if pet.name == target_pet:
                    pet.add_task(new_task)
                    break
            st.success(f"Task '{task_desc}' added for {target_pet}!")

    # -----------------------------------------------------------------------
    # Section 4: Today's Schedule
    # -----------------------------------------------------------------------

    st.header("Today's Schedule")

    if not owner.pets:
        st.info("No pets or tasks yet.")
    else:
        scheduler = Scheduler(owner)

        # Filter controls
        col1, col2 = st.columns(2)
        with col1:
            filter_pet = st.selectbox(
                "Filter by pet",
                ["All pets"] + [p.name for p in owner.pets]
            )
        with col2:
            filter_status = st.selectbox(
                "Filter by status",
                ["All", "pending", "complete"]
            )

        # Conflict warnings
        conflicts = scheduler.detect_conflicts()
        for warning in conflicts:
            st.warning(f"⚠️ {warning}")

        # Apply filters then sort
        pet_filter    = None if filter_pet == "All pets" else filter_pet
        status_filter = None if filter_status == "All" else filter_status
        filtered_tasks = scheduler.filter_tasks(status=status_filter, pet_name=pet_filter)
        sorted_tasks   = sorted(filtered_tasks, key=lambda t: t.time)

        if not sorted_tasks:
            st.info("No tasks match the current filters.")
        else:
            st.table([
                {
                    "Time":      t.time,
                    "Pet":       t.pet_name,
                    "Task":      t.description,
                    "Frequency": t.frequency,
                    "Status":    t.status,
                }
                for t in sorted_tasks
            ])

        # Mark complete
        st.subheader("Mark a Task Complete")
        pending_tasks = scheduler.filter_tasks(status="pending")
        if not pending_tasks:
            st.info("No pending tasks.")
        else:
            task_labels = [
                f"{t.time} — [{t.pet_name}] {t.description}"
                for t in pending_tasks
            ]
            selected_label = st.selectbox("Select task to complete", task_labels)
            if st.button("Mark complete"):
                idx = task_labels.index(selected_label)
                scheduler.mark_complete(pending_tasks[idx])
                st.success(f"'{pending_tasks[idx].description}' marked complete!")
                if pending_tasks[idx].frequency in ("daily", "weekly"):
                    st.info("Recurring task — next occurrence scheduled automatically.")
                st.rerun()
