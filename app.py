import re

import streamlit as st

from pawpal_system import Owner, Pet, Task, TimeSlot, PriorityLevel, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

PRIORITY_OPTIONS = {
    "Low": PriorityLevel.LOW,
    "Medium": PriorityLevel.MEDIUM,
    "High": PriorityLevel.HIGH,
}

TIME_PATTERN = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def is_valid_time(value: str) -> bool:
    """True if value is a valid 24-hour HH:MM time string."""
    return bool(TIME_PATTERN.match(value.strip()))


def check_time_conflict(new_slot: TimeSlot, existing_slots) -> bool:
    """True if new_slot overlaps any of the existing TimeSlots."""
    return any(new_slot.conflicts_with(slot) for slot in existing_slots)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "signup"
if "time_slots" not in st.session_state:
    st.session_state.time_slots = []  # list of (start, end) tuples (signup only)
if "pets" not in st.session_state:
    st.session_state.pets = []  # list of {"name", "species"} dicts (signup only)
if "owner" not in st.session_state:
    st.session_state.owner = None
if "owner_pets" not in st.session_state:
    st.session_state.owner_pets = []  # list of Pet objects
if "tasks" not in st.session_state:
    st.session_state.tasks = []  # list of Task objects
if "schedule" not in st.session_state:
    st.session_state.schedule = None  # dict[TimeSlot, List[Task]] once generated


# ===========================================================================
# SIGNUP SCREEN
# ===========================================================================
def render_signup():
    st.title("🐾 PawPal+")
    st.markdown(
        """
Welcome to **PawPal+**, a pet care planning assistant.

Start by signing up as an owner: enter your info, the time slots you're available
during the day, and the pets you care for.
"""
    )

    st.divider()

    # Owner info
    st.subheader("1. Your Info")
    owner_name = st.text_input("Owner name", value="", placeholder="e.g. Jordan")
    preference_choice = st.radio(
        "When do you prefer to care for your pets?",
        ["Morning", "Night", "Neither"],
        horizontal=True,
        index=2,
    )
    # "Neither" maps to no preference (None).
    preference = None if preference_choice == "Neither" else preference_choice.lower()

    # Available time slots
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
            start = slot_start.strip()
            end = slot_end.strip()
            if not is_valid_time(start) or not is_valid_time(end):
                st.warning("Please enter times in HH:MM format (e.g. 09:00).")
            elif start >= end:
                st.warning("Start time must be before end time.")
            else:
                new_slot = TimeSlot(start, end)
                existing = [TimeSlot(s, e) for s, e in st.session_state.time_slots]
                if check_time_conflict(new_slot, existing):
                    st.warning("This time slot conflicts with an existing slot.")
                else:
                    st.session_state.time_slots.append((start, end))

    if st.session_state.time_slots:
        for i, (start, end) in enumerate(st.session_state.time_slots):
            cols = st.columns([4, 1])
            cols[0].write(f"🕒 {start} – {end}")
            if cols[1].button("Remove", key=f"remove_slot_{i}"):
                st.session_state.time_slots.pop(i)
                st.rerun()
    else:
        st.info("No time slots yet. Add one above.")

    # Pets
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

    # Sign up
    st.subheader("4. Complete Sign Up")
    if st.button("Sign up", type="primary"):
        if not owner_name.strip():
            st.error("Please enter an owner name.")
        elif not st.session_state.time_slots:
            st.error("Please add at least one available time slot.")
        elif not st.session_state.pets:
            st.error("Please add at least one pet.")
        else:
            time_slots = sorted([TimeSlot(start, end) for start, end in st.session_state.time_slots], key = lambda x: x.start_time, reverse = True)
            if preference is None:
                owner = Owner(owner_name.strip(), time_slots)
            else:
                owner = Owner(owner_name.strip(), time_slots, preference=preference)
            pets = [Pet(p["name"], owner, p["species"]) for p in st.session_state.pets]
            st.session_state.owner = owner
            st.session_state.owner_pets = pets
            st.session_state.tasks = []
            st.session_state.page = "dashboard"
            st.rerun()


# ===========================================================================
# DASHBOARD SCREEN
# ===========================================================================
def add_pet_form(owner):
    st.markdown("#### Add a Pet")
    with st.form("add_pet_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 2])
        with col1:
            name = st.text_input("Pet name", placeholder="e.g. Mochi")
        with col2:
            species = st.selectbox("Species", ["dog", "cat", "other"])
        submitted = st.form_submit_button("Add pet")

    if submitted:
        if not name.strip():
            st.error("Please enter a pet name.")
        else:
            pet = Pet(name.strip(), owner, species)
            st.session_state.owner_pets.append(pet)
            st.success(f"Added pet: {pet.get_name()}")
            st.rerun()


def add_task_form(owner):
    pets = st.session_state.owner_pets
    pet_names = [pet.get_name() for pet in pets]

    st.markdown("#### Add a Task")
    if not pet_names:
        st.info("Add a pet first before creating tasks.")
        return

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
            owner.add_task(task)
            st.success(f"Added task: {task.get_name()}")
            st.rerun()


def render_schedule(owner):
    st.markdown("#### 📅 Your Daily Schedule")
    st.caption("Built from your tasks, priorities, and available time.")

    with st.expander("How is my schedule decided?"):
        st.write(Scheduler.explain_choice())

    # (Re)generate the schedule only when the user asks for it. Marking a task
    # complete does NOT rebuild the schedule, so completed tasks stay in place.
    if st.button(
        "Reset Schedule",  
        type="primary",
        help="This will generate a new schedule with your incomplete and recurring tasks.",
    ):
        # Recurring tasks reset to incomplete for the new schedule.
        for task in owner.get_tasks():
            if task.get_is_recurring():
                task.set_completed(False)
        st.session_state.schedule = Scheduler.create_daily_schedule(owner, owner.get_tasks())
        st.rerun()

    schedule = st.session_state.schedule
    if schedule is None:
        st.info("Click **Generate / Refresh schedule** to build your day.")
        return

    any_scheduled = any(tasks for tasks in schedule.values())
    if not any_scheduled:
        st.info("Nothing scheduled. Add some tasks, then refresh the schedule.")
        return

    for slot_index, (slot, slot_tasks) in enumerate(schedule.items()):
        st.markdown(f"**🕒 {slot.start_time} – {slot.end_time}**")
        if not slot_tasks:
            st.write("_(free)_")
            continue
        used = sum(t.get_duration_minutes() for t in slot_tasks)
        st.caption(f"{used} / {slot.duration_minutes()} min used")
        for task_index, task in enumerate(slot_tasks):
            pet_label = ", ".join(p.get_name() for p in task.get_pets())
            recurring = " 🔁" if task.get_is_recurring() else ""
            status = "✅ " if task.get_completed() else ""
            label = (
                f"{status}**{task.get_name()}**{recurring} "
                f"({task.get_duration_minutes()} min, "
                f"{task.get_priority().name.title()} priority) — {pet_label}"
            )
            checked = st.checkbox(
                label,
                value=task.get_completed(),
                key=f"complete_{slot_index}_{task_index}_{id(task)}",
            )
            # Only toggle completion state — do not regenerate the schedule.
            if checked != task.get_completed():
                task.set_completed(checked)
                st.rerun()

    # Tasks that didn't fit anywhere in the last generated schedule
    scheduled_ids = {id(t) for tasks in schedule.values() for t in tasks}
    unscheduled = [t for t in owner.get_tasks() if id(t) not in scheduled_ids]
    if unscheduled:
        st.warning("These tasks didn't fit in any available time slot:")
        for task in unscheduled:
            st.write(f"- {task.get_name()} ({task.get_duration_minutes()} min)")


def render_task_list(owner):
    st.markdown("#### Your Tasks")
    if not st.session_state.tasks:
        st.info("No tasks yet. Add one above.")
        return

    priority_names = list(PRIORITY_OPTIONS.keys())
    all_pet_names = [pet.get_name() for pet in st.session_state.owner_pets]

    for i, task in enumerate(st.session_state.tasks):
        header = f"{task.get_name()} — {task.get_priority().name.title()} priority"
        with st.expander(header):
            # --- Edit form ---
            with st.form(f"edit_task_form_{i}"):
                new_name = st.text_input("Task name", value=task.get_name())

                col_a, col_b = st.columns(2)
                with col_a:
                    new_duration = st.number_input(
                        "Duration (minutes)",
                        min_value=1,
                        max_value=240,
                        value=task.get_duration_minutes(),
                    )
                with col_b:
                    current_priority = task.get_priority().name.title()
                    new_priority = st.selectbox(
                        "Priority",
                        priority_names,
                        index=priority_names.index(current_priority),
                    )

                current_pets = [p.get_name() for p in task.get_pets()]
                new_pet_names = st.multiselect(
                    "Which pet(s) is this for?", all_pet_names, default=current_pets
                )

                col_c, col_d = st.columns(2)
                with col_c:
                    new_recurring = st.checkbox("Recurring", value=task.get_is_recurring())
                with col_d:
                    new_completed = st.checkbox("Completed", value=task.get_completed())

                new_notes = st.text_area("Notes (optional)", value=task.get_notes())

                saved = st.form_submit_button("Save changes")

            if saved:
                if not new_name.strip():
                    st.error("Please enter a task name.")
                elif not new_pet_names:
                    st.error("Please select at least one pet for this task.")
                else:
                    task_pets = [
                        p for p in st.session_state.owner_pets if p.get_name() in new_pet_names
                    ]
                    task.set_name(new_name.strip())
                    task.set_duration_minutes(int(new_duration))
                    task.set_priority(PRIORITY_OPTIONS[new_priority])
                    task.set_pets(task_pets)
                    task.set_is_recurring(new_recurring)
                    task.set_completed(new_completed)
                    task.set_notes(new_notes.strip())
                    st.success("Task updated.")
                    st.rerun()

            # --- Remove ---
            if st.button("Remove", key=f"remove_task_{i}"):
                removed = st.session_state.tasks.pop(i)
                owner.remove_task(removed)
                if st.session_state.schedule is not None:
                    for slot_tasks in st.session_state.schedule.values():
                        if removed in slot_tasks:
                            slot_tasks.remove(removed)
                st.rerun()


def render_dashboard():
    owner = st.session_state.owner

    st.title(f"🐾 Welcome, {owner.get_name()}!")
    st.caption(f"Total available time today: {owner.total_available_minutes()} minutes")

    # Schedule is generated and shown first
    render_schedule(owner)

    st.divider()

    # Manage pets and tasks
    tab_tasks, tab_pets = st.tabs(["Tasks", "Pets"])

    with tab_tasks:
        add_task_form(owner)
        st.divider()
        render_task_list(owner)

    with tab_pets:
        st.write("**Current pets:**")
        for pet in st.session_state.owner_pets:
            st.write(f"- 🐾 {pet.get_name()} ({pet.get_species()})")
        st.divider()
        add_pet_form(owner)

    st.divider()
    if st.button("Log out"):
        st.session_state.page = "signup"
        st.session_state.owner = None
        st.session_state.owner_pets = []
        st.session_state.tasks = []
        st.session_state.time_slots = []
        st.session_state.pets = []
        st.session_state.schedule = None
        st.rerun()


# ===========================================================================
# ROUTER
# ===========================================================================
if st.session_state.page == "dashboard" and st.session_state.owner is not None:
    render_dashboard()
else:
    render_signup()
