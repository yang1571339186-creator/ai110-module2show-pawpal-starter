from enum import Enum
from typing import List


class PriorityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class TimeSlot:
    def __init__(self, start_time: str, end_time: str):
        self.start_time = start_time
        self.end_time = end_time

    @staticmethod
    def parse(time_string: str) -> 'TimeSlot':
        parts = time_string.split('-')
        start = parts[0].strip()
        end = parts[1].strip()
        return TimeSlot(start, end)

    def duration_minutes(self) -> int:
        start_h, start_m = map(int, self.start_time.split(':'))
        end_h, end_m = map(int, self.end_time.split(':'))
        start_total = start_h * 60 + start_m
        end_total = end_h * 60 + end_m
        return end_total - start_total

    def conflicts_with(self, other: 'TimeSlot') -> bool:
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)

    def __eq__(self, other) -> bool:
        if not isinstance(other, TimeSlot):
            return NotImplemented
        return self.start_time == other.start_time and self.end_time == other.end_time

    def __hash__(self) -> int:
        return hash((self.start_time, self.end_time))

    def __repr__(self) -> str:
        return f"TimeSlot({self.start_time}-{self.end_time})"


class Owner:
    def __init__(self, name: str, available_time_slots: List[TimeSlot], tasks: List['Task'] = None):
        self.name = name
        self.available_time_slots = available_time_slots
        self.tasks = tasks if tasks is not None else []

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_available_time_slots(self) -> List[TimeSlot]:
        return self.available_time_slots

    def set_available_time_slots(self, available_time_slots: List[TimeSlot]) -> None:
        self.available_time_slots = available_time_slots

    def get_tasks(self) -> List['Task']:
        return self.tasks

    def set_tasks(self, tasks: List['Task']) -> None:
        self.tasks = tasks

    def add_task(self, task: 'Task') -> None:
        self.tasks.append(task)

    def remove_task(self, task: 'Task') -> None:
        self.tasks.remove(task)

    def total_available_minutes(self) -> int:
        return sum(slot.duration_minutes() for slot in self.available_time_slots)

    def __repr__(self) -> str:
        slots_str = ', '.join([str(slot) for slot in self.available_time_slots])
        return f"Owner(name='{self.name}', available_time_slots=[{slots_str}], tasks={len(self.tasks)})"


class Pet:
    def __init__(self, name: str, owner: 'Owner', species: str):
        self.name = name
        self.owner = owner
        self.species = species

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_owner(self) -> 'Owner':
        return self.owner

    def set_owner(self, owner: 'Owner') -> None:
        self.owner = owner

    def get_species(self) -> str:
        return self.species

    def set_species(self, species: str) -> None:
        self.species = species

    def __repr__(self) -> str:
        return f"Pet(name='{self.name}', owner={self.owner.name}, species='{self.species}')"


class Task:
    def __init__(self, name: str, pets: List[Pet], duration_minutes: int,
                 priority: PriorityLevel, is_recurring: bool, completed: bool = False, notes: str = ""):
        self.name = name
        self.pets = pets
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.is_recurring = is_recurring
        self.completed = completed
        self.notes = notes

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_pets(self) -> List[Pet]:
        return self.pets

    def set_pets(self, pets: List[Pet]) -> None:
        self.pets = pets

    def get_duration_minutes(self) -> int:
        return self.duration_minutes

    def set_duration_minutes(self, duration: int) -> None:
        self.duration_minutes = duration

    def get_priority(self) -> PriorityLevel:
        return self.priority

    def set_priority(self, priority: PriorityLevel) -> None:
        self.priority = priority

    def get_is_recurring(self) -> bool:
        return self.is_recurring

    def set_is_recurring(self, is_recurring: bool) -> None:
        self.is_recurring = is_recurring

    def get_completed(self) -> bool:
        return self.completed

    def set_completed(self, completed: bool) -> None:
        self.completed = completed

    def get_notes(self) -> str:
        return self.notes

    def set_notes(self, notes: str) -> None:
        self.notes = notes

    def __repr__(self) -> str:
        pet_names = ', '.join([p.name for p in self.pets]) if self.pets else 'None'
        return f"Task(name='{self.name}', pets=[{pet_names}], duration_minutes={self.duration_minutes}, priority={self.priority.value}, is_recurring={self.is_recurring}, completed={self.completed})"


class Scheduler:
    @staticmethod
    def sort_tasks_by_priority(tasks: List[Task], completed: bool = False) -> List[Task]:
        filtered_tasks = [
            task for task in tasks
            if task.get_is_recurring() or task.get_completed() == completed
        ]
        return sorted(filtered_tasks, key=lambda task: task.get_priority().value, reverse=True)

    @staticmethod
    def filter_tasks_by_time(tasks: List[Task], available_minutes: int) -> List[Task]:
        filtered_tasks = [task for task in tasks if task.get_duration_minutes() <= available_minutes]
        return Scheduler.sort_tasks_by_priority(filtered_tasks)

    @staticmethod
    def create_daily_schedule(owner: Owner, tasks: List[Task]) -> dict:
        schedule = {}
        placed = set()
        for slot in owner.get_available_time_slots():
            schedule[slot] = []
            remaining = [task for task in tasks if id(task) not in placed]
            candidates = Scheduler.filter_tasks_by_time(remaining, slot.duration_minutes())
            used = 0
            for task in candidates:
                if used + task.get_duration_minutes() <= slot.duration_minutes():
                    schedule[slot].append(task)
                    used += task.get_duration_minutes()
                    placed.add(id(task))
        return schedule

    @staticmethod
    def explain_choice(task: Task, reason: str) -> str:
        pass
