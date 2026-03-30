from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import List, Optional


class Priority(Enum):
    """Enumeration for task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Pet:
    """Represents a pet owned by a user"""
    pet_id: str
    name: str
    species: str
    breed: str
    age: float
    weight: float

    def get_pet_info(self) -> None:
        pass

    def update_pet_info(self, data: dict) -> None:
        pass


@dataclass
class Task:
    """Represents a pet care task"""
    task_id: str
    title: str
    description: str
    priority: Priority
    duration: int  # in minutes
    due_date: datetime
    is_completed: bool = False

    def set_priority(self, priority: Priority) -> None:
        pass

    def set_duration(self, duration: int) -> None:
        pass

    def mark_complete(self) -> None:
        pass

    def update_task(self, data: dict) -> None:
        pass


@dataclass
class DailyPlan:
    """Represents a daily plan containing tasks for a specific date"""
    plan_id: str
    date: datetime
    tasks: List[Task]

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass

    def reorder_tasks(self, order: List[str]) -> None:
        pass


@dataclass
class Notification:
    """Represents a notification for a task"""
    notification_id: str
    task_id: str
    user_id: str
    message: str
    sent_at: datetime
    is_read: bool = False

    def mark_as_read(self) -> None:
        pass

    def send_reminder(self) -> None:
        pass


class User:
    """Represents a user of the PawPal app"""

    def __init__(self, user_id: str, username: str, email: str, password: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = datetime.now()
        self.pets: List[Pet] = []
        self.calendar: Optional['Calendar'] = None

    def get_user_info(self) -> None:
        pass

    def update_profile(self, data: dict) -> None:
        pass

    def delete_account(self) -> None:
        pass


class Calendar:
    """Represents a calendar structure holding daily plans"""

    def __init__(self, calendar_id: str, user_id: str):
        self.calendar_id = calendar_id
        self.user_id = user_id
        self.daily_plans: List[DailyPlan] = []

    def create_daily_plan(self, date: datetime) -> None:
        pass

    def get_daily_plan(self, date: datetime) -> Optional[DailyPlan]:
        pass

    def get_month_view(self, month: int) -> List[DailyPlan]:
        pass

    def get_week_view(self, week: int) -> List[DailyPlan]:
        pass

    def delete_day(self, date: datetime) -> None:
        pass
