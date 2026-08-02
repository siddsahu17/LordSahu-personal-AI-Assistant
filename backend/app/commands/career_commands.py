from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class LogJobApplicationCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        company_name = params.get("company_name") or "Company"
        role_title = params.get("role_title") or "AI Engineer"

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="career",
            source="chat_text",
            event_type="JOB_APPLIED",
            intent="LOG_JOB_APP",
            payload={"company_name": company_name, "role_title": role_title}
        ))
        return {
            "status": "success",
            "company_name": company_name,
            "event_id": evt.id,
            "message": f"Logged job application to '{company_name}' ({role_title}) into Career Journal."
        }

class LogResumeUpdateCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        summary = params.get("summary") or "Updated resume experience section"
        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="career",
            source="chat_text",
            event_type="RESUME_UPDATED",
            intent="LOG_RESUME",
            payload={"summary": summary}
        ))
        return {"status": "success", "event_id": evt.id, "message": f"Logged resume update: '{summary}'."}
