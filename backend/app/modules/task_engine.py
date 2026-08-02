import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import TaskModel
from app.schemas import TaskCreate

DEFAULT_TASKS = [
    {
        "title": "DBMS Assignment on SQL Joins & Subqueries",
        "workspace_id": "learning",
        "priority": "HIGH",
        "due_date": datetime.now(timezone.utc) + timedelta(hours=8)
    },
    {
        "title": "Cardio & Weight Check-in",
        "workspace_id": "fitness",
        "priority": "MEDIUM",
        "due_date": datetime.now(timezone.utc) + timedelta(hours=18)
    },
    {
        "title": "Review LordSahu Mission Control Dashboard",
        "workspace_id": "projects",
        "priority": "LOW",
        "due_date": datetime.now(timezone.utc) + timedelta(days=1)
    }
]

class TaskEngine:
    """
    Task Engine manages scheduled tasks, reminders, and recurring habits.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self._ensure_defaults()

    def _ensure_defaults(self):
        count = self.db.query(TaskModel).filter(TaskModel.user_id == self.user_id).count()
        if count == 0:
            for t in DEFAULT_TASKS:
                db_task = TaskModel(
                    id=str(uuid.uuid4()),
                    user_id=self.user_id,
                    workspace_id=t["workspace_id"],
                    title=t["title"],
                    priority=t["priority"],
                    due_date=t["due_date"],
                    status="PENDING"
                )
                self.db.add(db_task)
            self.db.commit()

    def create_task(self, task_data: TaskCreate) -> TaskModel:
        db_task = TaskModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            workspace_id=task_data.workspace_id,
            title=task_data.title,
            due_date=task_data.due_date,
            priority=task_data.priority,
            status=task_data.status,
            recurring_rule=task_data.recurring_rule,
            related_goal_id=task_data.related_goal_id
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def list_tasks(self, workspace_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.db.query(TaskModel).filter(TaskModel.user_id == self.user_id)
        if workspace_id and workspace_id != "all":
            query = query.filter(TaskModel.workspace_id == workspace_id)
        if status:
            query = query.filter(TaskModel.status == status)
        tasks = query.order_by(TaskModel.created_at.desc()).all()

        return [
            {
                "id": t.id,
                "title": t.title,
                "workspace_id": t.workspace_id,
                "due_date": t.due_date.isoformat() if t.due_date else None,
                "priority": t.priority,
                "status": t.status,
                "recurring_rule": t.recurring_rule,
                "created_at": t.created_at.isoformat() if t.created_at else None
            }
            for t in tasks
        ]

    def update_task_status(self, task_id: str, new_status: str) -> Optional[Dict[str, Any]]:
        task = self.db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == self.user_id).first()
        if not task:
            return None
        task.status = new_status
        task.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        return {
            "id": task.id,
            "title": task.title,
            "status": task.status
        }
