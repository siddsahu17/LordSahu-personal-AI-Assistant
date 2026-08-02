import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import TaskModel
from app.schemas import TaskCreate

class TaskEngine:
    """
    Task Engine manages scheduled tasks and reminders directly in SQLite.
    No mock or dummy tasks are seeded.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

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

    def delete_task(self, task_identifier: str) -> Optional[str]:
        query = self.db.query(TaskModel).filter(TaskModel.user_id == self.user_id)
        task = query.filter(TaskModel.id == task_identifier).first()
        if not task:
            task = query.filter(TaskModel.title.ilike(f"%{task_identifier}%")).first()

        if task:
            deleted_title = task.title
            self.db.delete(task)
            self.db.commit()
            return deleted_title
        return None

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
