import json
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import EventModel
from app.schemas import EventCreate

class EventEngine:
    """
    Event Engine is the core store of truth. Every meaningful action creates a rich Event.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

    def create_event(self, event_data: EventCreate) -> EventModel:
        db_event = EventModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            workspace_id=event_data.workspace_id,
            source=event_data.source,
            event_type=event_data.event_type,
            intent=event_data.intent,
            entities=json.dumps(event_data.entities),
            payload=json.dumps(event_data.payload),
            confidence=event_data.confidence,
            created_by=event_data.created_by,
            parent_event_id=event_data.parent_event_id,
            related_goal_id=event_data.related_goal_id,
            attachments=json.dumps(event_data.attachments)
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def query_events(
        self,
        workspace_id: Optional[str] = None,
        event_type: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        query = self.db.query(EventModel).filter(EventModel.user_id == self.user_id)
        if workspace_id and workspace_id != "all":
            query = query.filter(EventModel.workspace_id == workspace_id)
        if event_type and event_type != "all":
            query = query.filter(EventModel.event_type == event_type)
        if search_query:
            pattern = f"%{search_query}%"
            query = query.filter(
                or_(
                    EventModel.event_type.ilike(pattern),
                    EventModel.intent.ilike(pattern),
                    EventModel.payload.ilike(pattern),
                    EventModel.entities.ilike(pattern)
                )
            )

        events = query.order_by(EventModel.created_at.desc()).limit(limit).all()
        results = []
        for e in events:
            try:
                entities_list = json.loads(e.entities)
            except Exception:
                entities_list = []
            try:
                payload_dict = json.loads(e.payload)
            except Exception:
                payload_dict = {}
            try:
                attachments_list = json.loads(e.attachments)
            except Exception:
                attachments_list = []

            results.append({
                "id": e.id,
                "user_id": e.user_id,
                "workspace_id": e.workspace_id,
                "source": e.source,
                "event_type": e.event_type,
                "intent": e.intent,
                "entities": entities_list,
                "payload": payload_dict,
                "confidence": e.confidence,
                "created_by": e.created_by,
                "parent_event_id": e.parent_event_id,
                "related_goal_id": e.related_goal_id,
                "attachments": attachments_list,
                "created_at": e.created_at.isoformat() if e.created_at else None
            })
        return results

    def get_life_timeline(self, search_query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Organizes events chronologically grouped into temporal buckets (Year -> Month -> Day).
        """
        raw_events = self.query_events(search_query=search_query, limit=200)
        grouped = {}
        for event in raw_events:
            dt_str = event["created_at"]
            if not dt_str:
                continue
            dt = datetime.fromisoformat(dt_str)
            date_key = dt.strftime("%Y-%m-%d")
            if date_key not in grouped:
                grouped[date_key] = {
                    "date": date_key,
                    "day_name": dt.strftime("%A"),
                    "formatted_date": dt.strftime("%B %d, %Y"),
                    "events": []
                }
            grouped[date_key]["events"].append(event)

        timeline_list = list(grouped.values())
        timeline_list.sort(key=lambda x: x["date"], reverse=True)
        return timeline_list
