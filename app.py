import streamlit as st

from pawpal_system import Owner, Pet, Task, TimeSlot, PriorityLevel

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, a pet care planning assistant.

Start by signing up as an owner: enter your info, the time slots you're available
during the day, and the pets you care for.
"""
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "time_slots" not in st.session_state:
    st.session_state.time_slots = []  # list of (start, end) tuples
if "pets" not in st.session_state:
    st.session_state.pets = []  # list of {"name", "species"} dicts
if "owner" not in st.session_state:
    st.session_state.owner = None
if "owner_pets" not in st.session_state:
    st.session_state.owner_pets = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []  # list of Task objects

st.divider()

# ---------------------------------------------------------------------------
# Owner info
# ---------------------------------------------------------------------------
st.subheader("1. Your Info")
owner_name = st.text_input("Owner name", value="", placeholder="e.g. Jordan")

# ---------------------------------------------------------------------------
# Available time slots
# ---------------------------------------------------------------------------
st.subheader("2. Your Available Time Slots")
st.caption("When are you free to care for your pets today? Add one or more slots.")

slot_col1, slot_col2, slot_col3 = st.columns([2, 2, 1])
with slot_col1:
    slot_start = st.text_input("Start (HH:MM)", value="09:00", key="slot_start")
with slot_col2:
    slot_end = st.text_input("End (HH:MM)", value="17:00", key="slot_end")
with slot_col3:
    st.write("")
    st.write("")
    if st.button("Add slot"):
        if slot_start < slot_end:
            st.session_state.time_slots.append((slot_start, slot_end))
        else:
            st.warning("Start time must be before end time.")

if st.session_state.time_slots:
    for i, (start, end) in enumerate(st.session_state.time_slots):
        cols = st.columns([4, 1])
        cols[0].write(f"🕒 {start} – {end}")
        if cols[1].button("Remove", key=f"remove_slot_{i}"):
            st.session_state.time_slots.pop(i)
            st.rerun()
else:
    st.info("No time slots yet. Add one above.")

# ---------------------------------------------------------------------------
# Pets
# ---------------------------------------------------------------------------
st.subheader("3. Your Pets")
st.caption("Add each pet you care for.")

pet_col1, pet_col2, pet_col3 = st.columns([2, 2, 1])
with pet_col1:
    pet_name = st.text_input("Pet name", value="", placeholder="e.g. Mochi", key="pet_name")
with pet_col2:
    pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species")
with pet_col3:
    st.write("")
    st.write("")
    if st.button("Add pet"):
        if pet_name.strip():
            st.session_state.pets.append({"name": pet_name.strip(), "species": pet_species})
        else:
            st.warning("Please enter a pet name.")

if st.session_state.pets:
    for i, pet in enumerate(st.session_state.pets):
        cols = st.columns([4, 1])
        cols[0].write(f"🐾 {pet['name']} ({pet['species']})")
        if cols[1].button("Remove", key=f"remove_pet_{i}"):
            st.session_state.pets.pop(i)
            st.rerun()
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Sign up
# ---------------------------------------------------------------------------
st.subheader("4. Complete Sign Up")

if st.button("Sign up", type="primary"):
    if not owner_name.strip():
        st.error("Please enter an owner name.")
    elif not st.session_state.time_slots:
        st.error("Please add at least one available time slot.")
    elif not st.session_state.pets:
        st.error("Please add at least one pet.")
    else:
        time_slots = [TimeSlot(start, end) for start, end in st.session_state.time_slots]
        owner = Owner(owner_name.strip(), time_slots)
        pets = [Pet(p["name"], owner, p["species"]) for p in st.session_state.pets]
        st.session_state.owner = owner
        st.session_state.owner_pets = pets
        st.session_state.tasks = []
        st.success(f"Welcome, {owner.get_name()}! Your account is set up.")

# ---------------------------------------------------------------------------
# Summary of the signed-up owner
# ---------------------------------------------------------------------------
if st.session_state.owner is not None:
    owner = st.session_state.owner
    st.markdown("#### Your Profile")
    st.write(f"**Owner:** {owner.get_name()}")
    st.write(f"**Total available minutes:** {owner.total_available_minutes()}")

    st.write("**Available time slots:**")
    for slot in owner.get_available_time_slots():
        st.write(f"- {slot.start_time} – {slot.end_time} ({slot.duration_minutes()} min)")

    st.write("**Pets:**")
    for pet in st.session_state.get("owner_pets", []):
        st.write(f"- {pet.get_name()} ({pet.get_species()})")

    # -----------------------------------------------------------------------
    # Task entry
    # -----------------------------------------------------------------------
    st.divider()
    st.subheader("5. Add Care Tasks")
    st.caption("Add the tasks you need to do for your pets today.")

    PRIORITY_OPTIONS = {
        "Low": PriorityLevel.LOW,
        "Medium": PriorityLevel.MEDIUM,
        "High": PriorityLevel.HIGH,
    }
    pets = st.session_state.owner_pets
    pet_names = [pet.get_name() for pet in pets]

    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("Task name", placeholder="e.g. Morning walk")

        col_a, col_b = st.columns(2)
        with col_a:
            task_duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20
            )
        with col_b:
            task_priority = st.selectbox("Priority", list(PRIORITY_OPTIONS.keys()), index=2)

        selected_pet_names = st.multiselect(
            "Which pet(s) is this for?", pet_names, default=pet_names[:1]
        )

        col_c, col_d = st.columns(2)
        with col_c:
            is_recurring = st.checkbox("Recurring", value=False)
        with col_d:
            completed = st.checkbox("Already completed", value=False)

        notes = st.text_area("Notes (optional)", placeholder="Anything to remember?")

        submitted = st.form_submit_button("Add task")

    if submitted:
        if not task_name.strip():
            st.error("Please enter a task name.")
        elif not selected_pet_names:
            st.error("Please select at least one pet for this task.")
        else:
            task_pets = [pet for pet in pets if pet.get_name() in selected_pet_names]
            task = Task(
                name=task_name.strip(),
                pets=task_pets,
                duration_minutes=int(task_duration),
                priority=PRIORITY_OPTIONS[task_priority],
                is_recurring=is_recurring,
                completed=completed,
                notes=notes.strip(),
            )
            st.session_state.tasks.append(task)
            st.session_state.owner.add_task(task)
            st.success(f"Added task: {task.get_name()}")

    # Current tasks
    if st.session_state.tasks:
        st.write("**Current tasks:**")
        for i, task in enumerate(st.session_state.tasks):
            pet_label = ", ".join(p.get_name() for p in task.get_pets())
            header = f"{task.get_name()} — {task.get_priority().name.title()} priority"
            with st.expander(header):
                st.write(f"**Pets:** {pet_label}")
                st.write(f"**Duration:** {task.get_duration_minutes()} min")
                st.write(f"**Recurring:** {'Yes' if task.get_is_recurring() else 'No'}")
                st.write(f"**Completed:** {'Yes' if task.get_completed() else 'No'}")
                if task.get_notes():
                    st.write(f"**Notes:** {task.get_notes()}")
                if st.button("Remove", key=f"remove_task_{i}"):
                    removed = st.session_state.tasks.pop(i)
                    st.session_state.owner.remove_task(removed)
                    st.rerun()
    else:
        st.info("No tasks yet. Add one above.")
