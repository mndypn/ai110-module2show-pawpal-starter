from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")

# Create the backend objects once and keep them in the session vault so they
# (and every task added to them) survive Streamlit's reruns.
if "owner" not in st.session_state:
    pet = Pet(name="Mochi", age=3, species="dog")
    owner = Owner(name="Jordan")
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler

owner.name = st.text_input("Owner name", value=owner.name)

# --- Add a new pet ---------------------------------------------------------
# A form batches its inputs and only runs on submit, so the pet is created
# exactly once per click (not on every keystroke).
with st.form("add_pet", clear_on_submit=True):
    st.markdown("**Add a pet**")
    new_pet_name = st.text_input("Name", value="")
    new_pet_age = st.number_input("Age", min_value=0, max_value=40, value=1)
    new_pet_species = st.selectbox("Species ", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if new_pet_name.strip():
            # This is the call the whole feature is about: hand a freshly
            # built Pet to the persistent Owner via Owner.add_pet().
            owner.add_pet(Pet(name=new_pet_name, age=int(new_pet_age), species=new_pet_species))
            st.success(f"Added pet: {new_pet_name}")
        else:
            st.error("Please enter a pet name.")

# --- Pick which pet to work with -------------------------------------------
pet_names = [p.name for p in owner.pets]
selected_index = st.selectbox(
    "Active pet",
    range(len(owner.pets)),
    format_func=lambda i: pet_names[i],
)
pet = owner.pets[selected_index]

# Keep the selected pet in sync with the edit fields.
pet.name = st.text_input("Pet name", value=pet.name)
pet.age = st.number_input("Pet age", min_value=0, max_value=40, value=pet.age)
pet.species = st.selectbox(
    "Species",
    ["dog", "cat", "other"],
    index=["dog", "cat", "other"].index(pet.species)
    if pet.species in ["dog", "cat", "other"]
    else 2,
)

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed directly into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
task_due = st.date_input("Due date", value=date.today())

if st.button("Add task"):
    # Build a Task object and attach it to the pet via Pet.add_task().
    task = Task(
        description=task_title,
        due_date=task_due,
        priority=priority,
        duration=int(duration),
    )
    pet.add_task(task)
    st.success(f"Added task: {task.description}")

# Show every task across all of the owner's pets via Owner.view_tasks().
current_tasks = owner.view_tasks()
if current_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "title": t.description,
                "due_date": t.due_date,
                "duration_minutes": t.duration,
                "priority": t.priority,
                "done": t.completion_status,
            }
            for t in current_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Chooses and orders tasks that fit within your available time.")

available = st.number_input(
    "Available minutes today", min_value=0, max_value=1440, value=60
)

if st.button("Generate schedule"):
    # Call the scheduling logic on the persistent owner.
    plan = scheduler.build_schedule(owner, available_minutes=int(available))

    if plan:
        st.write(f"Planned {len(plan)} task(s) into {int(available)} minutes:")
        used = 0
        for i, task in enumerate(plan, start=1):
            used += task.duration
            st.markdown(
                f"**{i}. {task.description}** — {task.duration} min, "
                f"priority *{task.priority}*, due {task.due_date} "
                f"(runs because it fits the remaining time budget)"
            )
        st.caption(f"Total time used: {used} / {int(available)} minutes.")
    else:
        st.warning(
            "No tasks fit the plan. Add tasks above, or increase the available minutes."
        )
