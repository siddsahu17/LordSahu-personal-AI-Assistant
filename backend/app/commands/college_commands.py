from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class LogLectureCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        subject = params.get("subject") or "DBMS"
        attended = params.get("attended", True)

        evt_engine = EventEngine(self.db, self.user_id)
        evt_type = "LECTURE_ATTENDED" if attended else "LECTURE_MISSED"
        evt = evt_engine.create_event(EventCreate(
            workspace_id="college",
            source="chat_text",
            event_type=evt_type,
            intent="LOG_LECTURE",
            payload={"subject": subject, "attended": attended}
        ))
        status_str = "attended" if attended else "missed"
        return {
            "status": "success",
            "subject": subject,
            "event_id": evt.id,
            "message": f"Logged {status_str} lecture for '{subject}' into College Journal."
        }

class LogAssignmentCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        title = params.get("title") or "Assignment"
        subject = params.get("subject") or "Academics"
        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="college",
            source="chat_text",
            event_type="ASSIGNMENT_COMPLETED",
            intent="LOG_ASSIGNMENT",
            payload={"title": title, "subject": subject}
        ))
        return {"status": "success", "event_id": evt.id, "message": f"Logged completed assignment '{title}' ({subject})."}
