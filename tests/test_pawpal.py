import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pawpal_system import TimeSlot, Owner, Pet, Task, PriorityLevel, Scheduler


class TestTimeSlot:
    def test_timeslot_creation(self):
        slot = TimeSlot("09:00", "17:00")
        assert slot.start_time == "09:00"
        assert slot.end_time == "17:00"

    def test_timeslot_parse_valid(self):
        slot = TimeSlot.parse("09:00-17:00")
        assert slot.start_time == "09:00"
        assert slot.end_time == "17:00"

    def test_timeslot_parse_with_spaces(self):
        slot = TimeSlot.parse("9:00 - 17:00")
        assert slot.start_time == "9:00"
        assert slot.end_time == "17:00"

    def test_duration_minutes_one_hour(self):
        slot = TimeSlot("09:00", "10:00")
        assert slot.duration_minutes() == 60

    def test_duration_minutes_thirty_minutes(self):
        slot = TimeSlot("09:00", "09:30")
        assert slot.duration_minutes() == 30

    def test_duration_minutes_eight_hours(self):
        slot = TimeSlot("09:00", "17:00")
        assert slot.duration_minutes() == 480

    def test_duration_minutes_with_mixed_times(self):
        slot = TimeSlot("14:30", "16:45")
        assert slot.duration_minutes() == 135

    def test_conflicts_with_overlapping_start(self):
        slot1 = TimeSlot("09:00", "11:00")
        slot2 = TimeSlot("10:00", "12:00")
        assert slot1.conflicts_with(slot2) is True

    def test_conflicts_with_overlapping_end(self):
        slot1 = TimeSlot("10:00", "12:00")
        slot2 = TimeSlot("09:00", "11:00")
        assert slot1.conflicts_with(slot2) is True

    def test_conflicts_with_completely_overlapping(self):
        slot1 = TimeSlot("09:00", "17:00")
        slot2 = TimeSlot("10:00", "12:00")
        assert slot1.conflicts_with(slot2) is True

    def test_conflicts_with_no_overlap_before(self):
        slot1 = TimeSlot("09:00", "11:00")
        slot2 = TimeSlot("12:00", "14:00")
        assert slot1.conflicts_with(slot2) is False

    def test_conflicts_with_no_overlap_after(self):
        slot1 = TimeSlot("12:00", "14:00")
        slot2 = TimeSlot("09:00", "11:00")
        assert slot1.conflicts_with(slot2) is False

    def test_conflicts_with_adjacent_times(self):
        slot1 = TimeSlot("09:00", "11:00")
        slot2 = TimeSlot("11:00", "13:00")
        assert slot1.conflicts_with(slot2) is False

    def test_timeslot_repr(self):
        slot = TimeSlot("09:00", "17:00")
        assert repr(slot) == "TimeSlot(09:00-17:00)"


class TestScheduler:
    @pytest.fixture
    def setup_owner_and_pet(self):
        owner = Owner("Alice", [TimeSlot("09:00", "17:00")])
        pet = Pet("Buddy", owner, "dog")
        return owner, pet

    def test_sort_tasks_by_priority_single_high(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [
            Task("High Priority Task", [pet], 30, PriorityLevel.HIGH, False)
        ]
        sorted_tasks = Scheduler.sort_tasks_by_priority(tasks)
        assert sorted_tasks[0].get_priority() == PriorityLevel.HIGH

    def test_sort_tasks_by_priority_mixed_order(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [
            Task("Low Priority", [pet], 30, PriorityLevel.LOW, False),
            Task("High Priority", [pet], 30, PriorityLevel.HIGH, False),
            Task("Medium Priority", [pet], 30, PriorityLevel.MEDIUM, False),
        ]
        sorted_tasks = Scheduler.sort_tasks_by_priority(tasks)
        assert sorted_tasks[0].get_priority() == PriorityLevel.HIGH
        assert sorted_tasks[1].get_priority() == PriorityLevel.MEDIUM
        assert sorted_tasks[2].get_priority() == PriorityLevel.LOW

    def test_sort_tasks_by_priority_all_same(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [
            Task("Task 1", [pet], 30, PriorityLevel.MEDIUM, False),
            Task("Task 2", [pet], 30, PriorityLevel.MEDIUM, False),
            Task("Task 3", [pet], 30, PriorityLevel.MEDIUM, False),
        ]
        sorted_tasks = Scheduler.sort_tasks_by_priority(tasks)
        assert all(task.get_priority() == PriorityLevel.MEDIUM for task in sorted_tasks)

    def test_sort_tasks_by_priority_empty_list(self):
        sorted_tasks = Scheduler.sort_tasks_by_priority([])
        assert sorted_tasks == []

    def test_sort_tasks_by_priority_multiple_high_and_low(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [
            Task("High 1", [pet], 30, PriorityLevel.HIGH, False),
            Task("Low 1", [pet], 30, PriorityLevel.LOW, False),
            Task("High 2", [pet], 30, PriorityLevel.HIGH, False),
            Task("Low 2", [pet], 30, PriorityLevel.LOW, False),
        ]
        sorted_tasks = Scheduler.sort_tasks_by_priority(tasks)
        assert sorted_tasks[0].get_priority() == PriorityLevel.HIGH
        assert sorted_tasks[1].get_priority() == PriorityLevel.HIGH
        assert sorted_tasks[2].get_priority() == PriorityLevel.LOW
        assert sorted_tasks[3].get_priority() == PriorityLevel.LOW

    def test_sort_tasks_by_priority_defaults_to_incomplete(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [
            Task("Done", [pet], 30, PriorityLevel.HIGH, False, completed=True),
            Task("Todo", [pet], 30, PriorityLevel.LOW, False, completed=False),
        ]
        sorted_tasks = Scheduler.sort_tasks_by_priority(tasks)
        assert len(sorted_tasks) == 1
        assert sorted_tasks[0].get_name() == "Todo"

    def test_sort_tasks_by_priority_completed_only(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [
            Task("Done High", [pet], 30, PriorityLevel.HIGH, False, completed=True),
            Task("Done Low", [pet], 30, PriorityLevel.LOW, False, completed=True),
            Task("Todo", [pet], 30, PriorityLevel.HIGH, False, completed=False),
        ]
        sorted_tasks = Scheduler.sort_tasks_by_priority(tasks, completed=True)
        assert len(sorted_tasks) == 2
        assert sorted_tasks[0].get_name() == "Done High"
        assert sorted_tasks[1].get_name() == "Done Low"

    def test_sort_tasks_by_priority_recurring_always_included(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [
            Task("Recurring Done", [pet], 30, PriorityLevel.HIGH, True, completed=True),
            Task("Todo", [pet], 30, PriorityLevel.LOW, False, completed=False),
        ]
        # Default (incomplete) still includes the completed recurring task.
        sorted_tasks = Scheduler.sort_tasks_by_priority(tasks)
        names = [task.get_name() for task in sorted_tasks]
        assert names == ["Recurring Done", "Todo"]

    def test_sort_tasks_by_priority_recurring_incomplete_in_completed_view(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [
            Task("Recurring Todo", [pet], 30, PriorityLevel.HIGH, True, completed=False),
            Task("Done", [pet], 30, PriorityLevel.LOW, False, completed=True),
        ]
        # completed=True view still includes the incomplete recurring task.
        sorted_tasks = Scheduler.sort_tasks_by_priority(tasks, completed=True)
        names = [task.get_name() for task in sorted_tasks]
        assert names == ["Recurring Todo", "Done"]


class TestCreateDailySchedule:
    @pytest.fixture
    def setup_owner_and_pet(self):
        owner = Owner("Alice", [TimeSlot("09:00", "17:00")])
        pet = Pet("Buddy", owner, "dog")
        return owner, pet

    def test_returns_dict_keyed_by_time_slots(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [Task("Morning Walk", [pet], 30, PriorityLevel.HIGH, False)]
        schedule = Scheduler.create_daily_schedule(owner, tasks)

        assert isinstance(schedule, dict)
        assert set(schedule.keys()) == set(owner.get_available_time_slots())

    def test_no_tasks_gives_empty_lists(self, setup_owner_and_pet):
        owner, _ = setup_owner_and_pet
        schedule = Scheduler.create_daily_schedule(owner, [])

        for tasks in schedule.values():
            assert tasks == []

    def test_task_placed_into_available_slot(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        task = Task("Morning Walk", [pet], 30, PriorityLevel.HIGH, False)
        schedule = Scheduler.create_daily_schedule(owner, [task])

        slot = owner.get_available_time_slots()[0]
        assert task in schedule[slot]

    def test_all_fitting_tasks_scheduled(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        tasks = [
            Task("Morning Walk", [pet], 30, PriorityLevel.HIGH, False),
            Task("Feeding", [pet], 15, PriorityLevel.HIGH, False),
            Task("Playtime", [pet], 45, PriorityLevel.MEDIUM, False),
        ]
        schedule = Scheduler.create_daily_schedule(owner, tasks)

        scheduled = [t for slot_tasks in schedule.values() for t in slot_tasks]
        assert set(scheduled) == set(tasks)

    def test_higher_priority_scheduled_first(self, setup_owner_and_pet):
        owner, pet = setup_owner_and_pet
        low = Task("Playtime", [pet], 30, PriorityLevel.LOW, False)
        high = Task("Morning Walk", [pet], 30, PriorityLevel.HIGH, False)
        schedule = Scheduler.create_daily_schedule(owner, [low, high])

        slot = owner.get_available_time_slots()[0]
        assert schedule[slot].index(high) < schedule[slot].index(low)

    def test_task_too_long_not_scheduled(self):
        owner = Owner("Alice", [TimeSlot("09:00", "09:30")])
        pet = Pet("Buddy", owner, "dog")
        task = Task("Long Task", [pet], 60, PriorityLevel.HIGH, False)
        schedule = Scheduler.create_daily_schedule(owner, [task])

        scheduled = [t for slot_tasks in schedule.values() for t in slot_tasks]
        assert task not in scheduled

    def test_slot_capacity_respected(self):
        owner = Owner("Alice", [TimeSlot("09:00", "10:00")])
        pet = Pet("Buddy", owner, "dog")
        tasks = [
            Task("A", [pet], 40, PriorityLevel.HIGH, False),
            Task("B", [pet], 40, PriorityLevel.HIGH, False),
        ]
        schedule = Scheduler.create_daily_schedule(owner, tasks)

        slot = owner.get_available_time_slots()[0]
        total = sum(t.get_duration_minutes() for t in schedule[slot])
        assert total <= slot.duration_minutes()
