from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.repositories.goal_repository import GoalRepository
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class CreateGoalCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        title = params.get("title") or "New Goal"
        workspace_id = params.get("workspace_id") or "personal"
        target_value = float(params.get("target_value") or 10.0)

        repo = GoalRepository(self.db)
        goal = repo.add(repo.model_cls(
            user_id=self.user_id,
            workspace_id=workspace_id,
            title=title,
            target_value=target_value,
            target_metric="hours",
            priority="HIGH"
        ))

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id=workspace_id,
            source="chat_text",
            event_type="GOAL_CREATED",
            intent="CREATE_GOAL",
            entities=[{"type": "goal_title", "value": title}],
            payload={"goal_id": goal.id, "title": title}
        ))
        return {
            "status": "success",
            "goal_id": goal.id,
            "title": goal.title,
            "event_id": evt.id,
            "message": f"Created goal '{title}' in {workspace_id} workspace."
        }

class DeleteGoalCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        title = params.get("title")
        repo = GoalRepository(self.db)
        goal = repo.find_by_title_or_id(self.user_id, title)
        if goal:
            deleted_title = goal.title
            repo.delete(goal)
            evt_engine = EventEngine(self.db, self.user_id)
            evt_engine.create_event(EventCreate(
                workspace_id=goal.workspace_id,
                source="chat_text",
                event_type="GOAL_DELETED",
                intent="DELETE_GOAL",
                payload={"title": deleted_title}
            ))
            return {"status": "success", "message": f"Deleted goal '{deleted_title}'."}
        return {"status": "error", "message": f"Goal '{title}' not found."}
