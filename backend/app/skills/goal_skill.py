from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.goal_commands import CreateGoalCommand, DeleteGoalCommand

class CreateGoalTool(BaseTool):
    name = "create_goal"
    description = "Create a new living goal in LordSahu database."
    category = "goals"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = CreateGoalCommand(db, user_id)
        return cmd.execute(params)

class DeleteGoalTool(BaseTool):
    name = "delete_goal"
    description = "Delete a living goal from LordSahu database."
    category = "goals"
    requires_permission = True

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = DeleteGoalCommand(db, user_id)
        return cmd.execute(params)

class GoalSkill(BaseSkill):
    name = "goal_skill"
    description = "Living Goal creation, progress tracking, and deletion management."

    def get_tools(self) -> List[BaseTool]:
        return [CreateGoalTool(), DeleteGoalTool()]
