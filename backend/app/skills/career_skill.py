from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.career_commands import LogJobApplicationCommand, LogResumeUpdateCommand

class LogJobAppTool(BaseTool):
    name = "log_job_app"
    description = "Log job application sent into Career Journal."
    category = "career"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogJobApplicationCommand(db, user_id)
        return cmd.execute(params)

class LogResumeTool(BaseTool):
    name = "log_resume"
    description = "Log resume update event."
    category = "career"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogResumeUpdateCommand(db, user_id)
        return cmd.execute(params)

class CareerSkill(BaseSkill):
    name = "career_skill"
    description = "Career Intelligence Module tools (applications, resume, certifications, interviews)."

    def get_tools(self) -> List[BaseTool]:
        return [LogJobAppTool(), LogResumeTool()]
