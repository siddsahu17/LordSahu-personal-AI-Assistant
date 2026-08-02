from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class LogConceptCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        concept_name = params.get("concept_name") or "Concept"
        subject = params.get("subject") or "Learning"

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="learning",
            source="chat_text",
            event_type="CONCEPT_LEARNED",
            intent="LOG_CONCEPT",
            payload={"concept_name": concept_name, "subject": subject}
        ))
        return {
            "status": "success",
            "concept_name": concept_name,
            "event_id": evt.id,
            "message": f"Logged learned concept '{concept_name}' ({subject}) into Learning Journal."
        }

class LogProblemCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        problem_title = params.get("problem_title") or "Problem"
        difficulty = params.get("difficulty") or "Medium"

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="learning",
            source="chat_text",
            event_type="PROBLEM_SOLVED",
            intent="LOG_PROBLEM",
            payload={"problem_title": problem_title, "difficulty": difficulty}
        ))
        return {
            "status": "success",
            "problem_title": problem_title,
            "event_id": evt.id,
            "message": f"Logged solved problem '{problem_title}' [{difficulty}] into Learning Journal."
        }
