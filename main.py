from datetime import date
from pawpal_system import Owner, Pet, Task, TimeSlot, PriorityLevel

# Initialize TimeSlots for Owner 1
owner1_slots = [TimeSlot("09:00", "17:00")]

# Initialize Owner 1
owner1 = Owner("Alice", owner1_slots)

# Initialize Pet 1 for Owner 1
pet1_owner1 = Pet("Buddy", owner1, "dog")

# Initialize 3 Tasks for Pet 1 (Owner 1)
task1_owner1 = Task(
    name="Morning Walk",
    pets=[pet1_owner1],
    duration_minutes=30,
    priority=PriorityLevel.HIGH,
    is_recurring=True,
    notes="Before breakfast"
)

task2_owner1 = Task(
    name="Feeding",
    pets=[pet1_owner1],
    duration_minutes=15,
    priority=PriorityLevel.HIGH,
    is_recurring=True,
    notes="Dog food"
)

task3_owner1 = Task(
    name="Playtime",
    pets=[pet1_owner1],
    duration_minutes=45,
    priority=PriorityLevel.MEDIUM,
    is_recurring=True,
    notes="Interactive toys"
)

owner1.set_tasks([task1_owner1, task2_owner1, task3_owner1])

# Initialize TimeSlots for Owner 2
owner2_slots = [TimeSlot("08:00", "18:00")]

# Initialize Owner 2
owner2 = Owner("Bob", owner2_slots)

# Initialize Pet 1 for Owner 2
pet1_owner2 = Pet("Whiskers", owner2, "cat")

# Initialize 3 Tasks for Pet 1 (Owner 2)
task1_owner2 = Task(
    name="Litter Box Cleaning",
    pets=[pet1_owner2],
    duration_minutes=10,
    priority=PriorityLevel.HIGH,
    is_recurring=True,
    notes="Daily cleaning"
)

task2_owner2 = Task(
    name="Feeding",
    pets=[pet1_owner2],
    duration_minutes=10,
    priority=PriorityLevel.HIGH,
    is_recurring=True,
    notes="Cat food"
)

task3_owner2 = Task(
    name="Grooming",
    pets=[pet1_owner2],
    duration_minutes=20,
    priority=PriorityLevel.MEDIUM,
    is_recurring=False,
    notes="Brush fur"
)

owner2.set_tasks([task1_owner2, task2_owner2, task3_owner2])

# Print information
print("=" * 60)
print("OWNER 1: Alice")
print("=" * 60)
print(owner1)
print(f"  Total available minutes: {owner1.total_available_minutes()}")
print()
print(f"  Pet: {pet1_owner1}")
print()
print("  Tasks:")
print(f"    1. {task1_owner1}")
print(f"    2. {task2_owner1}")
print(f"    3. {task3_owner1}")

print()
print("=" * 60)
print("OWNER 2: Bob")
print("=" * 60)
print(owner2)
print(f"  Total available minutes: {owner2.total_available_minutes()}")
print()
print(f"  Pet: {pet1_owner2}")
print()
print("  Tasks:")
print(f"    1. {task1_owner2}")
print(f"    2. {task2_owner2}")
print(f"    3. {task3_owner2}")

print()
print("=" * 60)
print("All objects initialized successfully!")
print("=" * 60)
