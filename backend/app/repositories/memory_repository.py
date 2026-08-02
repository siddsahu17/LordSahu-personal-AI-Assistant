from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import MemoryModel
from app.repositories.base_repository import BaseRepository

class MemoryRepository(BaseRepository[MemoryModel]):
    def __init__(self, db: Session):
        super().__init__(db, MemoryModel)

    def list_memories(
        self,
        user_id: str = "default_user",
        memory_type: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[MemoryModel]:
        query = self.db.query(MemoryModel).filter(MemoryModel.user_id == user_id)
        if memory_type and memory_type != "ALL":
            query = query.filter(MemoryModel.memory_type == memory_type)
        if category and category != "ALL":
            query = query.filter(MemoryModel.category == category)
        return query.order_by(MemoryModel.created_at.desc()).all()

    def find_by_fact_or_id(self, user_id: str, identifier: str) -> Optional[MemoryModel]:
        query = self.db.query(MemoryModel).filter(MemoryModel.user_id == user_id)
        mem = query.filter(MemoryModel.id == identifier).first()
        if not mem:
            mem = query.filter(MemoryModel.fact.ilike(f"%{identifier}%")).first()
        return mem

    def touch_memory(self, memory: MemoryModel) -> None:
        memory.last_used = datetime.now(timezone.utc)
        memory.times_used = (memory.times_used or 0) + 1
        self.db.commit()
