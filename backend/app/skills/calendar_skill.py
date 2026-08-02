from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.calendar_commands import CreateCalendarEventCommand, DeleteCalendarEventCommand
from app.services.calendar_provider import calendar_provider

class CreateCalendarEventTool(BaseTool):
    name = "create_calendar_event"
    description = "Schedule activity into Google Calendar."
    category = "calendar"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = CreateCalendarEventCommand(db, user_id)
        return cmd.execute(params)

class DeleteCalendarEventTool(BaseTool):
    name = "delete_calendar_event"
    description = "Remove activity from Google Calendar."
    category = "calendar"
    requires_permission = True

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = DeleteCalendarEventCommand(db, user_id)
        return cmd.execute(params)

class QueryCalendarTool(BaseTool):
    name = "query_calendar"
    description = "Query upcoming events from Google Calendar."
    category = "calendar"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        evts = calendar_provider.list_upcoming_events()
        return {"status": "success", "upcoming_calendar": evts}

class CalendarSkill(BaseSkill):
    name = "calendar_skill"
    description = "Google Calendar integration, scheduled activities, and calendar queries."

    def get_tools(self) -> List[BaseTool]:
        return [CreateCalendarEventTool(), DeleteCalendarEventTool(), QueryCalendarTool()]
