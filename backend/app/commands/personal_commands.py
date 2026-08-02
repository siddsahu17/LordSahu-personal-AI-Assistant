from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class LogJournalEntryCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        text = params.get("text") or "Daily Reflection"
        mood = params.get("mood") or "Positive"

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="personal",
            source="chat_text",
            event_type="JOURNAL_ENTRY",
            intent="LOG_JOURNAL",
            payload={"text": text, "mood": mood}
        ))
        return {
            "status": "success",
            "event_id": evt.id,
            "message": f"Logged journal reflection into Personal Life Journal."
        }

class LogMoodCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        mood = params.get("mood") or "Great"
        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="personal",
            source="chat_text",
            event_type="MOOD_LOGGED",
            intent="LOG_MOOD",
            payload={"mood": mood}
        ))
        return {"status": "success", "event_id": evt.id, "message": f"Logged mood '{mood}' into Personal Journal."}
