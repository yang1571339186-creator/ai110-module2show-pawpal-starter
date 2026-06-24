from enum import Enum
from datetime import date
from typing import List


class PriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Owner:
    def __init__(self, name: str, available_time_slot: str):
        self.name = name
        self.available_time_slot = available_time_slot


class Pet:
    def __init__(self, name: str, owner: str, species: str):
        self.name = name
        self.owner = owner
        self.species = species

    def set_name(self, name: str) -> None:
        pass

    def set_owner(self, owner: str) -> None:
        pass

    def set_species(self, species: str) -> None:
        pass


class Task:
    def __init__(self, name: str, pets: List[Pet], duration_minutes: int,
                 priority: PriorityLevel, recurring: str):
        self.name = name
        self.pets = pets
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.recurring = recurring

    def set_name(self, name: str) -> None:
        pass

    def set_pets(self, pets: List[Pet]) -> None:
        pass

    def set_duration_minutes(self, duration: int) -> None:
        pass

    def set_priority(self, priority: PriorityLevel) -> None:
        pass

    def set_recurring(self, recurring: str) -> None:
        pass


class Schedule:
    def __init__(self, owner: Owner, tasks: List[Task], plan_date: date):
        self.owner = owner
        self.tasks = tasks
        self.plan_date = plan_date

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def generate_plan(self) -> List:
        pass

    def get_plan(self) -> List:
        pass


class Scheduler:
    @staticmethod
    def sort_by_priority(tasks: List[Task]) -> List[Task]:
        pass

    @staticmethod
    def filter_by_available_time(tasks: List[Task], available_minutes: int) -> List[Task]:
        pass

    @staticmethod
    def handle_conflicts(tasks: List[Task]) -> List[Task]:
        pass

    @staticmethod
    def create_schedule(owner: Owner, pets: List[Pet], tasks: List[Task],
                       available_minutes: int) -> List:
        pass
