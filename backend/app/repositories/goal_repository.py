from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import GoalModel
from app.repositories.base_repository import BaseRepository

class GoalRepository(BaseRepository[GoalModel]):
    def __init__(self, db: Session):
        super().__init__(db, GoalModel)

    def list_goals(self, user_id: str = "default_user", workspace_id: Optional[str] = None) -> List[GoalModel]:
        query = self.db.query(GoalModel).filter(GoalModel.user_id == user_id)
        if workspace_id and workspace_id != "all":
            query = query.filter(GoalModel.workspace_id == workspace_id)
        return query.order_by(GoalModel.created_at.desc()).all()

    def find_by_title_or_id(self, user_id: str, identifier: str) -> Optional[GoalModel]:
        query = self.db.query(GoalModel).filter(GoalModel.user_id == user_id)
        goal = query.filter(GoalModel.id == identifier).first()
        if not goal:
            goal = query.filter(GoalModel.title.ilike(f"%{identifier}%")).first()
        return goal
