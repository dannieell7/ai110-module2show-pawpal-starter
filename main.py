from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler, Frequency


def main():
    """Main script to demonstrate the PawPal system"""

    # Create a Scheduler (the brain of our system)
    scheduler = Scheduler()

    # Create an Owner
    owner = Owner(owner_id="O001", name="Alex", email="alex@pawpal.com")
    scheduler.add_owner(owner)

    # Create Pets
    pet1 = Pet(pet_id="P001", name="Buddy", species="Dog", breed="Golden Retriever", age=3.5, weight=70)
    pet2 = Pet(pet_id="P002", name="Whiskers", species="Cat", breed="Siamese", age=2.0, weight=8)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Create Tasks with different times for today
    today = datetime.now()
    
    # Task 1: Morning feeding for Buddy
    task1 = Task(
        task_id="T001",
        description="Feed Buddy breakfast",
        time=today.replace(hour=8, minute=0, second=0, microsecond=0),
        frequency=Frequency.DAILY,
        is_completed=False
    )

    # Task 2: Midday walk for Buddy
    task2 = Task(
        task_id="T002",
        description="Walk Buddy in the park",
        time=today.replace(hour=12, minute=30, second=0, microsecond=0),
        frequency=Frequency.DAILY,
        is_completed=False
    )

    # Task 3: Evening feeding for Buddy
    task3 = Task(
        task_id="T003",
        description="Feed Buddy dinner",
        time=today.replace(hour=18, minute=0, second=0, microsecond=0),
        frequency=Frequency.DAILY,
        is_completed=False
    )

    # Task 4: Litter box cleaning for Whiskers
    task4 = Task(
        task_id="T004",
        description="Clean Whiskers' litter box",
        time=today.replace(hour=9, minute=0, second=0, microsecond=0),
        frequency=Frequency.DAILY,
        is_completed=False
    )

    # Task 5: Feeding Whiskers
    task5 = Task(
        task_id="T005",
        description="Feed Whiskers",
        time=today.replace(hour=17, minute=30, second=0, microsecond=0),
        frequency=Frequency.DAILY,
        is_completed=False
    )

    # Add tasks to pets
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet1.add_task(task3)
    
    pet2.add_task(task4)
    pet2.add_task(task5)

    # Print Owner Info
    print("=" * 60)
    print("PAWPAL - PET CARE MANAGEMENT SYSTEM")
    print("=" * 60)
    print("\nOwner Information:")
    owner_info = owner.get_owner_info()
    print(f"  Name: {owner_info['name']}")
    print(f"  Email: {owner_info['email']}")
    print(f"  Total Pets: {owner_info['total_pets']}")
    print(f"  Total Tasks: {owner_info['total_tasks']}")
    print(f"  Pending Tasks: {owner_info['pending_tasks']}")

    # Print Pet Info
    print("\nPets Information:")
    for pet in owner.get_all_pets():
        pet_info = pet.get_pet_info()
        print(f"\n  {pet_info['name']} ({pet_info['species']} - {pet_info['breed']})")
        print(f"    Age: {pet_info['age']} years | Weight: {pet_info['weight']} lbs")
        print(f"    Tasks: {pet_info['total_tasks']} total, {pet_info['completed_tasks']} completed")

    # Print Today's Schedule
    print("\n" + "=" * 60)
    print("TODAY'S SCHEDULE")
    print("=" * 60)
    print(f"Date: {today.strftime('%A, %B %d, %Y')}\n")

    # Get tasks sorted by time
    tasks_today = scheduler.get_sorted_tasks_for_owner(owner.owner_id)
    
    if tasks_today:
        for i, task in enumerate(tasks_today, 1):
            status = "✓ DONE" if task.is_completed else "⏳ PENDING"
            time_str = task.time.strftime("%I:%M %p")
            print(f"{i}. [{time_str}] {task.description}")
            print(f"   Frequency: {task.frequency.value.upper()} | Status: {status}\n")
    else:
        print("No tasks scheduled for today.")

    # Print Completion Summary
    print("=" * 60)
    print("TODAY'S SUMMARY")
    print("=" * 60)
    summary = scheduler.get_completion_summary(owner.owner_id)
    print(f"Total Tasks: {summary['total_tasks']}")
    print(f"Completed: {summary['completed_tasks']}")
    print(f"Pending: {summary['pending_tasks']}")
    print(f"Completion Rate: {summary['completion_rate']}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
