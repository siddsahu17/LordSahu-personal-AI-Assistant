from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import TaskModel
from app.repositories.base_repository import BaseRepository

class TaskRepository(BaseRepository[TaskModel]):
    def __init__(self, db: Session):
        super().__init__(db, TaskModel)

    def list_tasks(
        self,
        user_id: str = "default_user",
        workspace_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[TaskModel]:
        query = self.db.query(TaskModel).filter(TaskModel.user_id == user_id)
        if workspace_id and workspace_id != "all":
            query = query.filter(TaskModel.workspace_id == workspace_id)
        if status:
            query = query.filter(TaskModel.status == status)
        return query.order_by(TaskModel.created_at.desc()).all()

    def find_by_title_or_id(self, user_id: str, identifier: str) -> Optional[TaskModel]:
        query = self.db.query(TaskModel).filter(TaskModel.user_id == user_id)
        task = query.filter(TaskModel.id == identifier).first()
        if not task:
            task = query.filter(TaskModel.title.ilike(f"%{identifier}%")).first()
        return task
