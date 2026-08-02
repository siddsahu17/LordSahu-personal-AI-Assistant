from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.college_commands import LogLectureCommand, LogAssignmentCommand

class LogLectureTool(BaseTool):
    name = "log_lecture"
    description = "Log college lecture attended or missed."
    category = "college"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogLectureCommand(db, user_id)
        return cmd.execute(params)

class LogAssignmentTool(BaseTool):
    name = "log_assignment"
    description = "Log completed academic assignment."
    category = "college"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogAssignmentCommand(db, user_id)
        return cmd.execute(params)

class CollegeSkill(BaseSkill):
    name = "college_skill"
    description = "College Intelligence Module tools (lectures, attendance, assignments, exams)."

    def get_tools(self) -> List[BaseTool]:
        return [LogLectureTool(), LogAssignmentTool()]
