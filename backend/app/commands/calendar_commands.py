from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.services.calendar_provider import calendar_provider
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class CreateCalendarEventCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        title = params.get("title") or "Scheduled Activity"
        start_time = params.get("start_time") or "Tomorrow 9:00 AM"
        end_time = params.get("end_time")
        description = params.get("description") or "Scheduled by LordSahu AI OS"
        workspace_id = params.get("workspace_id") or "personal"

        cal_evt = calendar_provider.create_event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
            workspace_id=workspace_id
        )

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id=workspace_id,
            source="chat_text",
            event_type="CALENDAR_EVENT_CREATED",
            intent="CREATE_CALENDAR_EVENT",
            payload={"calendar_event_id": cal_evt["id"], "title": title, "start_time": start_time}
        ))

        return {
            "status": "success",
            "calendar_event": cal_evt,
            "event_id": evt.id,
            "message": f"Created Google Calendar event '{title}' for {start_time}."
        }

class DeleteCalendarEventCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        title = params.get("title")
        success = calendar_provider.delete_event(title)
        return {
            "status": "success" if success else "not_found",
            "message": f"Removed calendar event '{title}'." if success else f"Calendar event '{title}' not found."
        }
