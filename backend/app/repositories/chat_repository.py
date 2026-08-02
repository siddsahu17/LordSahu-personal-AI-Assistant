from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import ChatMessageModel, ChatSessionModel
from app.repositories.base_repository import BaseRepository

class ChatRepository(BaseRepository[ChatMessageModel]):
    def __init__(self, db: Session):
        super().__init__(db, ChatMessageModel)

    def list_messages(
        self,
        user_id: str = "default_user",
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> List[ChatMessageModel]:
        query = self.db.query(ChatMessageModel).filter(ChatMessageModel.user_id == user_id)
        if session_id:
            query = query.filter(ChatMessageModel.session_id == session_id)
        return query.order_by(ChatMessageModel.created_at.asc()).limit(limit).all()

    def create_session(self, user_id: str = "default_user", title: str = "New Conversation", workspace_id: str = "personal") -> ChatSessionModel:
        session = ChatSessionModel(user_id=user_id, title=title, workspace_id=workspace_id)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def list_sessions(self, user_id: str = "default_user") -> List[ChatSessionModel]:
        return self.db.query(ChatSessionModel).filter(ChatSessionModel.user_id == user_id).order_by(ChatSessionModel.updated_at.desc()).all()
