from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Optional


class Frequency(Enum):
    """Enumeration for task frequency"""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    """Represents a single activity for a pet"""
    task_id: str
    description: str
    time: datetime  # when the task should be done
    frequency: Frequency
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed"""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed"""
        self.is_completed = False

    def reschedule(self, new_time: datetime) -> None:
        """Reschedule the task to a new time"""
        self.time = new_time

    def get_task_info(self) -> dict:
        """Returns task information as a dictionary"""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "time": self.time,
            "frequency": self.frequency.value,
            "is_completed": self.is_completed
        }


class Pet:
    """Represents a pet with its associated tasks"""

    def __init__(self, pet_id: str, name: str, species: str, breed: str, age: float, weight: float):
        self.pet_id = pet_id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.weight = weight
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list"""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task by task_id"""
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks for this pet"""
        return self.tasks

    def get_completed_tasks(self) -> List[Task]:
        """Return all completed tasks"""
        return [task for task in self.tasks if task.is_completed]

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks"""
        return [task for task in self.tasks if not task.is_completed]

    def get_pet_info(self) -> dict:
        """Returns pet information as a dictionary"""
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "weight": self.weight,
            "total_tasks": len(self.tasks),
            "completed_tasks": len(self.get_completed_tasks())
        }

    def update_pet_info(self, **kwargs) -> None:
        """Update pet information"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Owner:
    """Manages multiple pets and provides access to all their tasks"""

    def __init__(self, owner_id: str, name: str, email: str):
        self.owner_id = owner_id
        self.name = name
        self.email = email
        self.pets: List[Pet] = []
        self.created_at = datetime.now()

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection"""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet by pet_id"""
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """Get a specific pet by pet_id"""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def get_all_pets(self) -> List[Pet]:
        """Return all pets owned by this owner"""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets"""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_all_tasks())
        return all_tasks

    def get_all_pending_tasks(self) -> List[Task]:
        """Get all incomplete tasks across all pets"""
        pending_tasks = []
        for pet in self.pets:
            pending_tasks.extend(pet.get_pending_tasks())
        return pending_tasks

    def get_all_completed_tasks(self) -> List[Task]:
        """Get all completed tasks across all pets"""
        completed_tasks = []
        for pet in self.pets:
            completed_tasks.extend(pet.get_completed_tasks())
        return completed_tasks

    def get_tasks_by_pet(self, pet_id: str) -> List[Task]:
        """Get all tasks for a specific pet"""
        pet = self.get_pet(pet_id)
        if pet:
            return pet.get_all_tasks()
        return []

    def get_owner_info(self) -> dict:
        """Returns owner information"""
        return {
            "owner_id": self.owner_id,
            "name": self.name,
            "email": self.email,
            "total_pets": len(self.pets),
            "total_tasks": len(self.get_all_tasks()),
            "pending_tasks": len(self.get_all_pending_tasks())
        }


class Scheduler:
    """The "Brain" that retrieves, organizes, and manages tasks across pets"""

    def __init__(self):
        self.owners: List[Owner] = []

    def add_owner(self, owner: Owner) -> None:
        """Register an owner"""
        self.owners.append(owner)

    def remove_owner(self, owner_id: str) -> None:
        """Remove an owner"""
        self.owners = [owner for owner in self.owners if owner.owner_id != owner_id]

    def get_owner(self, owner_id: str) -> Optional[Owner]:
        """Get a specific owner"""
        for owner in self.owners:
            if owner.owner_id == owner_id:
                return owner
        return None

    def get_all_tasks_by_owner(self, owner_id: str) -> List[Task]:
        """Get all tasks for an owner"""
        owner = self.get_owner(owner_id)
        if owner:
            return owner.get_all_tasks()
        return []

    def get_tasks_due_today(self, owner_id: str) -> List[Task]:
        """Get all tasks due today for an owner"""
        owner = self.get_owner(owner_id)
        if not owner:
            return []

        today = datetime.now().date()
        tasks_due_today = []
        for task in owner.get_all_tasks():
            if task.time.date() == today:
                tasks_due_today.append(task)
        return tasks_due_today

    def get_tasks_due_this_week(self, owner_id: str) -> List[Task]:
        """Get all tasks due this week for an owner"""
        owner = self.get_owner(owner_id)
        if not owner:
            return []

        today = datetime.now().date()
        week_end = today + timedelta(days=7)
        tasks_this_week = []
        for task in owner.get_all_tasks():
            task_date = task.time.date()
            if today <= task_date <= week_end:
                tasks_this_week.append(task)
        return tasks_this_week

    def get_pending_tasks(self, owner_id: str) -> List[Task]:
        """Get all pending (incomplete) tasks for an owner"""
        owner = self.get_owner(owner_id)
        if owner:
            return owner.get_all_pending_tasks()
        return []

    def get_completed_tasks(self, owner_id: str) -> List[Task]:
        """Get all completed tasks for an owner"""
        owner = self.get_owner(owner_id)
        if owner:
            return owner.get_all_completed_tasks()
        return []

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by scheduled time (earliest first)"""
        return sorted(tasks, key=lambda task: task.time)

    def get_sorted_tasks_for_owner(self, owner_id: str) -> List[Task]:
        """Get all tasks for an owner sorted by time"""
        tasks = self.get_all_tasks_by_owner(owner_id)
        return self.sort_tasks_by_time(tasks)

    def mark_task_complete(self, owner_id: str, task_id: str) -> bool:
        """Mark a task as complete for an owner"""
        owner = self.get_owner(owner_id)
        if not owner:
            return False

        for task in owner.get_all_tasks():
            if task.task_id == task_id:
                task.mark_complete()
                return True
        return False

    def mark_task_incomplete(self, owner_id: str, task_id: str) -> bool:
        """Mark a task as incomplete for an owner"""
        owner = self.get_owner(owner_id)
        if not owner:
            return False

        for task in owner.get_all_tasks():
            if task.task_id == task_id:
                task.mark_incomplete()
                return True
        return False

    def get_completion_summary(self, owner_id: str) -> dict:
        """Get a summary of task completion status"""
        owner = self.get_owner(owner_id)
        if not owner:
            return {}

        all_tasks = owner.get_all_tasks()
        completed = owner.get_all_completed_tasks()
        pending = owner.get_all_pending_tasks()

        return {
            "total_tasks": len(all_tasks),
            "completed_tasks": len(completed),
            "pending_tasks": len(pending),
            "completion_rate": round(len(completed) / len(all_tasks) * 100, 2) if all_tasks else 0
        }
