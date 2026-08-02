import json
import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import EventModel
from app.schemas import EventCreate
from app.repositories.event_repository import EventRepository
from app.modules.event_bus import event_bus

class EventEngine:
    """
    Event Engine manages immutable life events in the Event Store.
    Publishes all created events to the internal EventBus.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self.repository = EventRepository(db)

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
            attachments=json.dumps(event_data.attachments),
            schema_version="1.0"
        )
        saved = self.repository.add(db_event)

        # Publish created event to internal Event Bus
        event_bus.publish(saved.event_type, {
            "id": saved.id,
            "user_id": saved.user_id,
            "workspace_id": saved.workspace_id,
            "event_type": saved.event_type,
            "intent": saved.intent,
            "payload": event_data.payload,
            "created_at": saved.created_at.isoformat() if saved.created_at else None
        })
        return saved

    def query_events(
        self,
        workspace_id: Optional[str] = None,
        event_type: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        events = self.repository.query_events(
            user_id=self.user_id,
            workspace_id=workspace_id,
            event_type=event_type,
            search=search,
            limit=limit
        )
        return [
            {
                "id": e.id,
                "user_id": e.user_id,
                "workspace_id": e.workspace_id,
                "source": e.source,
                "event_type": e.event_type,
                "intent": e.intent,
                "entities": json.loads(e.entities) if e.entities else [],
                "payload": json.loads(e.payload) if e.payload else {},
                "confidence": e.confidence,
                "created_by": e.created_by,
                "parent_event_id": e.parent_event_id,
                "related_goal_id": e.related_goal_id,
                "attachments": json.loads(e.attachments) if e.attachments else [],
                "schema_version": e.schema_version,
                "created_at": e.created_at.isoformat() if e.created_at else None
            }
            for e in events
        ]

    def get_life_timeline(self, workspace_id: Optional[str] = None, search_query: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.query_events(workspace_id=workspace_id, search=search_query, limit=50)
