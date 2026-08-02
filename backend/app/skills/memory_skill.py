from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.memory_commands import CreateMemoryCommand, DeleteMemoryCommand

class CreateMemoryTool(BaseTool):
    name = "create_memory"
    description = "Store a preference, habit, or fact memory in Memory Bank."
    category = "memory"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = CreateMemoryCommand(db, user_id)
        return cmd.execute(params)

class DeleteMemoryTool(BaseTool):
    name = "delete_memory"
    description = "Delete a stored memory fact from Memory Bank."
    category = "memory"
    requires_permission = True

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = DeleteMemoryCommand(db, user_id)
        return cmd.execute(params)

class MemorySkill(BaseSkill):
    name = "memory_skill"
    description = "Self-learning memory management, preferences, and facts."

    def get_tools(self) -> List[BaseTool]:
        return [CreateMemoryTool(), DeleteMemoryTool()]
