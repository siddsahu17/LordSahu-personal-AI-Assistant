from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class LogFeatureCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        feature_name = params.get("feature_name") or "Feature"
        project_name = params.get("project_name") or "LordSahu AI OS"

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="projects",
            source="chat_text",
            event_type="FEATURE_BUILT",
            intent="LOG_FEATURE",
            payload={"feature_name": feature_name, "project_name": project_name}
        ))
        return {
            "status": "success",
            "feature_name": feature_name,
            "event_id": evt.id,
            "message": f"Logged implemented feature '{feature_name}' ({project_name}) into Project Journal."
        }

class LogBugFixCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        bug_summary = params.get("bug_summary") or "Bug Fix"
        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="projects",
            source="chat_text",
            event_type="BUG_FIXED",
            intent="LOG_BUG_FIX",
            payload={"bug_summary": bug_summary}
        ))
        return {"status": "success", "event_id": evt.id, "message": f"Logged bug fix: '{bug_summary}'."}
