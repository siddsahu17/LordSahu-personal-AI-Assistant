import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models import MemoryModel
from app.schemas import MemoryCreate

DEFAULT_MEMORIES = [
    {
        "memory_type": "PREFERENCE",
        "category": "fitness",
        "fact": "User prefers morning workouts and daily weight logs",
        "confidence": 1.0
    },
    {
        "memory_type": "FACT",
        "category": "fitness",
        "fact": "Target body weight is 80.0 kg (Starting weight ~99.0 kg, current ~96.8 kg)",
        "confidence": 1.0
    },
    {
        "memory_type": "GOAL",
        "category": "learning",
        "fact": "Current primary learning goals: SQL Joins, DBMS course, and Database Design",
        "confidence": 1.0
    },
    {
        "memory_type": "RELATIONSHIP",
        "category": "learning",
        "fact": "SQL and DBMS belong to the Learning Workspace",
        "relationship_entity": "DBMS -> Learning Workspace",
        "confidence": 1.0
    },
    {
        "memory_type": "HABIT",
        "category": "fitness",
        "fact": "User tends to skip workouts on Thursdays if study load is high",
        "confidence": 0.85
    }
]

class MemoryEngine:
    """
    Memory Engine manages categorized, typed memories and retrieves permanent knowledge for personalization.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self._ensure_defaults()

    def _ensure_defaults(self):
        count = self.db.query(MemoryModel).filter(MemoryModel.user_id == self.user_id).count()
        if count == 0:
            for mem in DEFAULT_MEMORIES:
                db_mem = MemoryModel(
                    id=str(uuid.uuid4()),
                    user_id=self.user_id,
                    memory_type=mem["memory_type"],
                    category=mem["category"],
                    fact=mem["fact"],
                    relationship_entity=mem.get("relationship_entity"),
                    confidence=mem["confidence"]
                )
                self.db.add(db_mem)
            self.db.commit()

    def add_memory(self, memory_data: MemoryCreate) -> MemoryModel:
        # Check if identical fact already exists
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

    def list_memories(self, memory_type: Optional[str] = None, category: Optional[str] = None) -> List[MemoryModel]:
        query = self.db.query(MemoryModel).filter(MemoryModel.user_id == self.user_id)
        if memory_type:
            query = query.filter(MemoryModel.memory_type == memory_type)
        if category:
            query = query.filter(MemoryModel.category == category)
        return query.order_by(MemoryModel.created_at.desc()).all()

    def retrieve_relevant_memories(self, query_text: str, limit: int = 5) -> List[str]:
        """
        Retrieves top relevant memory facts based on keyword overlap or full text relevance.
        """
        all_memories = self.list_memories()
        query_words = set(query_text.lower().split())

        scored_memories = []
        for mem in all_memories:
            fact_words = set(mem.fact.lower().split())
            overlap = len(query_words.intersection(fact_words))
            # Boost score if category matches
            if mem.category.lower() in query_text.lower():
                overlap += 2
            scored_memories.append((overlap, mem.fact))

        scored_memories.sort(key=lambda x: x[0], reverse=True)
        # Always return at least top memories or default facts
        results = [fact for score, fact in scored_memories[:limit]]
        if not results:
            results = [mem.fact for mem in all_memories[:limit]]
        return results
