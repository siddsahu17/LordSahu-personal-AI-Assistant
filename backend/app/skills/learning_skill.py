from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.learning_commands import LogConceptCommand, LogProblemCommand

class LogConceptTool(BaseTool):
    name = "log_concept"
    description = "Log learned concept into Learning Journal."
    category = "learning"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogConceptCommand(db, user_id)
        return cmd.execute(params)

class LogProblemTool(BaseTool):
    name = "log_problem"
    description = "Log solved programming/LeetCode problem."
    category = "learning"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogProblemCommand(db, user_id)
        return cmd.execute(params)

class LogStudyTool(BaseTool):
    name = "log_study"
    description = "Log study session duration into Event Store."
    category = "learning"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        subject = params.get("subject") or "General Learning"
        duration_hours = float(params.get("duration_hours") or 1.0)

        from app.schemas import EventCreate
        from app.modules.event_engine import EventEngine
        evt_eng = EventEngine(db, user_id)
        evt = evt_eng.create_event(EventCreate(
            workspace_id="learning",
            source="chat_text",
            event_type="STUDY_SESSION",
            intent="LOG_STUDY",
            payload={"subject": subject, "duration_hours": duration_hours}
        ))
        return {"status": "success", "subject": subject, "duration_hours": duration_hours, "event_id": evt.id, "message": f"Logged {duration_hours}h study on '{subject}'."}

class LearningSkill(BaseSkill):
    name = "learning_skill"
    description = "Learning Intelligence Module tools (concepts, LeetCode, books, documentation)."

    def get_tools(self) -> List[BaseTool]:
        return [LogConceptTool(), LogProblemTool(), LogStudyTool()]
