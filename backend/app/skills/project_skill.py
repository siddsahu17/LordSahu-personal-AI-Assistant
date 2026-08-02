from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.project_commands import LogFeatureCommand, LogBugFixCommand

class LogFeatureTool(BaseTool):
    name = "log_feature"
    description = "Log implemented software feature into Project Journal."
    category = "projects"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogFeatureCommand(db, user_id)
        return cmd.execute(params)

class LogBugFixTool(BaseTool):
    name = "log_bug_fix"
    description = "Log resolved bug fix into Project Journal."
    category = "projects"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogBugFixCommand(db, user_id)
        return cmd.execute(params)

class ProjectSkill(BaseSkill):
    name = "project_skill"
    description = "Project Intelligence Module tools (features built, bugs fixed, refactorings, deployments)."

    def get_tools(self) -> List[BaseTool]:
        return [LogFeatureTool(), LogBugFixTool()]
