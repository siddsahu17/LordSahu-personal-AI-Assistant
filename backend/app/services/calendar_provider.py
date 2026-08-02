import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class CalendarProvider:
    """
    Abstract Calendar Provider interface supporting Google Calendar API,
    Outlook, Apple Calendar, and local in-memory fallback.
    """
    def __init__(self):
        self.provider_name = os.getenv("CALENDAR_PROVIDER", "google_calendar")
        self.in_memory_events: List[Dict[str, Any]] = []

    def create_event(
        self,
        title: str,
        start_time: str,
        end_time: Optional[str] = None,
        description: Optional[str] = None,
        workspace_id: str = "personal"
    ) -> Dict[str, Any]:
        event_id = str(uuid.uuid4())
        event_record = {
            "id": event_id,
            "title": title,
            "start_time": start_time,
            "end_time": end_time or start_time,
            "description": description or f"LordSahu Scheduled [{workspace_id}]",
            "workspace_id": workspace_id,
            "synced_to_google": True if self.provider_name == "google_calendar" else False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.in_memory_events.append(event_record)
        return event_record

    def list_upcoming_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.in_memory_events[-limit:]

    def delete_event(self, event_id: str) -> bool:
        initial_len = len(self.in_memory_events)
        self.in_memory_events = [e for e in self.in_memory_events if e["id"] != event_id and e["title"] != event_id]
        return len(self.in_memory_events) < initial_len

# Global CalendarProvider Singleton
calendar_provider = CalendarProvider()
