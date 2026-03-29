"""
app.py — PawPal+ Streamlit UI
Imports all logic from pawpal_system.py. No scheduling logic lives here.
"""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler  # Step 1: the connection

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Step 2: Application "memory" via st.session_state
# Think of session_state as a vault that survives page rerenders.
# We only create the Owner once — if it already exists in the vault, skip it.
# ---------------------------------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = None  # no owner yet until the form is submitted

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
        # Step 3: calling the actual Owner class from pawpal_system.py
        st.session_state.owner = Owner(name=owner_name, email=owner_email)
        st.rerun()  # refresh so the page shows the owner dashboard
else:
    owner: Owner = st.session_state.owner
    st.success(f"Welcome back, {owner.name}!")

    # -----------------------------------------------------------------------
    # Section 2: Add a pet
    # -----------------------------------------------------------------------

    st.header("Add a Pet")
    with st.form("pet_form"):
        pet_name    = st.text_input("Pet name",  value="Mochi")
        pet_species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])
        pet_age     = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
        add_pet_btn = st.form_submit_button("Add pet")

    if add_pet_btn:
        new_pet = Pet(name=pet_name, species=pet_species, age=int(pet_age))
        owner.add_pet(new_pet)   # calling the method we wrote in Phase 2
        st.success(f"{pet_name} added!")

    # -----------------------------------------------------------------------
    # Section 3: Add a task to a pet
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
            # Find the right Pet object and call its add_task() method
            for pet in owner.pets:
                if pet.name == target_pet:
                    pet.add_task(new_task)
                    break
            st.success(f"Task '{task_desc}' added for {target_pet}!")

    # -----------------------------------------------------------------------
    # Section 4: View the schedule
    # -----------------------------------------------------------------------

    st.header("Today's Schedule")
    if not owner.pets:
        st.info("No pets or tasks yet.")
    else:
        scheduler = Scheduler(owner)

        # Conflict warnings first
        conflicts = scheduler.detect_conflicts()
        for warning in conflicts:
            st.warning(warning)

        # Sorted schedule table
        sorted_tasks = scheduler.sort_by_time()
        if sorted_tasks:
            st.table([
                {
                    "Time":        t.time,
                    "Pet":         t.pet_name,
                    "Task":        t.description,
                    "Frequency":   t.frequency,
                    "Status":      t.status,
                }
                for t in sorted_tasks
            ])
        else:
            st.info("No tasks scheduled yet.")
