import json
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from app.models import LifeEntryModel

class LifeEntryRepository:
    """
    LifeEntry Repository Layer for LordSahu V1 AI Daily Journal.
    Manages CRUD and cross-domain querying for LifeEntryModel with soft-deletion and raw data retention.
    """
    def __init__(self, db: Session):
        self.db = db

    def add_entry(
        self,
        user_id: str = "default_user",
        domains: List[str] = None,
        category: str = "journal",
        title: str = "Journal Entry",
        raw_text: str = "",
        source_raw_transcript: Optional[str] = None,
        structured_data: Optional[Dict[str, Any]] = None,
        ai_summary: Optional[str] = None,
        confidence: float = 1.0,
        source: str = "text",
        attachments: List[str] = None,
        tags: List[str] = None,
        related_entry_ids: List[str] = None
    ) -> LifeEntryModel:
        if not domains:
            domains = ["personal"]
        if not title:
            title = raw_text[:50] or "Life Entry"

        entry = LifeEntryModel(
            user_id=user_id,
            timestamp=datetime.now(timezone.utc),
            domains=json.dumps(domains),
            category=category,
            title=title,
            raw_text=raw_text,
            source_raw_transcript=source_raw_transcript or raw_text,
            structured_data=json.dumps(structured_data or {}),
            ai_summary=ai_summary or raw_text,
            confidence=confidence,
            source=source,
            entry_status="active",
            attachments=json.dumps(attachments or []),
            tags=json.dumps(tags or []),
            related_entry_ids=json.dumps(related_entry_ids or [])
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def update_entry(self, entry_id: str, updates: Dict[str, Any]) -> Optional[LifeEntryModel]:
        entry = self.db.query(LifeEntryModel).filter(LifeEntryModel.id == entry_id).first()
        if not entry:
            return None

        for k, v in updates.items():
            if k in ("domains", "structured_data", "attachments", "tags", "related_entry_ids") and isinstance(v, (list, dict)):
                setattr(entry, k, json.dumps(v))
            elif hasattr(entry, k):
                setattr(entry, k, v)

        entry.entry_status = "edited"
        entry.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def soft_delete_entry(self, entry_id: str) -> bool:
        entry = self.db.query(LifeEntryModel).filter(LifeEntryModel.id == entry_id).first()
        if not entry:
            return False
        entry.entry_status = "deleted"
        entry.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        return True

    def query_entries(
        self,
        user_id: str = "default_user",
        domain: Optional[str] = None,
        category: Optional[str] = None,
        search_query: Optional[str] = None,
        status: str = "active",
        limit: int = 50
    ) -> List[LifeEntryModel]:
        q = self.db.query(LifeEntryModel).filter(LifeEntryModel.user_id == user_id)

        if status != "all":
            q = q.filter(LifeEntryModel.entry_status == status)

        if domain and domain != "all":
            q = q.filter(LifeEntryModel.domains.contains(domain))

        if category and category != "all":
            q = q.filter(LifeEntryModel.category == category)

        if search_query:
            term = f"%{search_query}%"
            q = q.filter(or_(
                LifeEntryModel.title.ilike(term),
                LifeEntryModel.raw_text.ilike(term),
                LifeEntryModel.ai_summary.ilike(term),
                LifeEntryModel.tags.ilike(term)
            ))

        return q.order_by(desc(LifeEntryModel.timestamp)).limit(limit).all()

    def get_today_entries(self, user_id: str = "default_user") -> List[LifeEntryModel]:
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.db.query(LifeEntryModel).filter(
            and_(
                LifeEntryModel.user_id == user_id,
                LifeEntryModel.entry_status != "deleted",
                LifeEntryModel.timestamp >= start_of_day
            )
        ).order_by(desc(LifeEntryModel.timestamp)).all()

    def get_recent_active_topic(self, user_id: str = "default_user") -> Optional[Dict[str, Any]]:
        """
        Retrieves recent topic for 'Continue where you left off' UX card.
        """
        recent = self.db.query(LifeEntryModel).filter(
            and_(
                LifeEntryModel.user_id == user_id,
                LifeEntryModel.entry_status != "deleted"
            )
        ).order_by(desc(LifeEntryModel.timestamp)).first()

        if recent:
            return {
                "id": recent.id,
                "title": recent.title,
                "category": recent.category,
                "domains": json.loads(recent.domains) if recent.domains else [],
                "raw_text": recent.raw_text,
                "timestamp": recent.timestamp.strftime("%b %d, %I:%M %p")
            }
        return None
