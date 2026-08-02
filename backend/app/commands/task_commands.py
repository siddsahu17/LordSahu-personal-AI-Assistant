from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.repositories.task_repository import TaskRepository
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class ScheduleTaskCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        title = params.get("title") or "Scheduled Task"
        workspace_id = params.get("workspace_id") or "personal"
        priority = params.get("priority") or "HIGH"

        repo = TaskRepository(self.db)
        task = repo.add(repo.model_cls(
            user_id=self.user_id,
            workspace_id=workspace_id,
            title=title,
            priority=priority
        ))

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id=workspace_id,
            source="chat_text",
            event_type="TASK_CREATED",
            intent="CREATE_TASK",
            payload={"task_id": task.id, "title": title}
        ))

        return {
            "status": "success",
            "task_id": task.id,
            "title": task.title,
            "event_id": evt.id,
            "message": f"Scheduled task '{title}'."
        }
