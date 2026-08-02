import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import MemoryModel
from app.schemas import MemoryCreate

class MemoryEngine:
    """
    Memory Engine manages categorized, typed memories directly stored in the database.
    No mock or dummy data is seeded.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

    def add_memory(self, memory_data: MemoryCreate) -> MemoryModel:
        # Check if identical memory fact already exists
        existing = (
            self.db.query(MemoryModel)
            .filter(
                MemoryModel.user_id == self.user_id,
                MemoryModel.memory_type == memory_data.memory_type,
                MemoryModel.fact == memory_data.fact
            )
            .first()
        )
        if existing:
            existing.confidence = max(existing.confidence, memory_data.confidence)
            self.db.commit()
            self.db.refresh(existing)
            return existing

        db_mem = MemoryModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            memory_type=memory_data.memory_type,
            category=memory_data.category,
            fact=memory_data.fact,
            relationship_entity=memory_data.relationship_entity,
            confidence=memory_data.confidence,
            source_event_id=memory_data.source_event_id
        )
        self.db.add(db_mem)
        self.db.commit()
        self.db.refresh(db_mem)
        return db_mem

    def delete_memory(self, memory_identifier: str) -> Optional[str]:
        query = self.db.query(MemoryModel).filter(MemoryModel.user_id == self.user_id)
        mem = query.filter(MemoryModel.id == memory_identifier).first()
        if not mem:
            mem = query.filter(MemoryModel.fact.ilike(f"%{memory_identifier}%")).first()

        if mem:
            deleted_fact = mem.fact
            self.db.delete(mem)
            self.db.commit()
            return deleted_fact
        return None

    def list_memories(self, memory_type: Optional[str] = None, category: Optional[str] = None) -> List[MemoryModel]:
        query = self.db.query(MemoryModel).filter(MemoryModel.user_id == self.user_id)
        if memory_type and memory_type != "ALL":
            query = query.filter(MemoryModel.memory_type == memory_type)
        if category and category != "all":
            query = query.filter(MemoryModel.category == category)
        return query.order_by(MemoryModel.created_at.desc()).all()

    def retrieve_relevant_memories(self, query_text: str, limit: int = 5) -> List[str]:
        all_memories = self.list_memories()
        if not all_memories:
            return []

        query_words = set(query_text.lower().split())
        scored_memories = []
        for mem in all_memories:
            fact_words = set(mem.fact.lower().split())
            overlap = len(query_words.intersection(fact_words))
            if mem.category and mem.category.lower() in query_text.lower():
                overlap += 2
            scored_memories.append((overlap, mem.fact))

        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [fact for score, fact in scored_memories[:limit] if score > 0] or [m.fact for m in all_memories[:limit]]
