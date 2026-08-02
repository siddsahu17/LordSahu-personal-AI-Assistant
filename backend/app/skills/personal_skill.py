from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.personal_commands import LogJournalEntryCommand, LogMoodCommand

class LogJournalTool(BaseTool):
    name = "log_journal"
    description = "Log life journal reflection into Personal Journal."
    category = "personal"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogJournalEntryCommand(db, user_id)
        return cmd.execute(params)

class LogMoodTool(BaseTool):
    name = "log_mood"
    description = "Log daily mood into Personal Journal."
    category = "personal"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogMoodCommand(db, user_id)
        return cmd.execute(params)

class PersonalSkill(BaseSkill):
    name = "personal_skill"
    description = "Personal Intelligence Module tools (daily life reflections, mood, habits, movies/books)."

    def get_tools(self) -> List[BaseTool]:
        return [LogJournalTool(), LogMoodTool()]
