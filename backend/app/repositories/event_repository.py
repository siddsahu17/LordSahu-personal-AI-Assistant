import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import EventModel
from app.repositories.base_repository import BaseRepository

class EventRepository(BaseRepository[EventModel]):
    def __init__(self, db: Session):
        super().__init__(db, EventModel)

    def query_events(
        self,
        user_id: str = "default_user",
        workspace_id: Optional[str] = None,
        event_type: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50
    ) -> List[EventModel]:
        query = self.db.query(EventModel).filter(EventModel.user_id == user_id)

        if workspace_id and workspace_id != "all":
            query = query.filter(EventModel.workspace_id == workspace_id)
        if event_type:
            query = query.filter(EventModel.event_type == event_type)
        if search:
            query = query.filter(EventModel.payload.ilike(f"%{search}%"))

        return query.order_by(EventModel.created_at.desc()).limit(limit).all()
