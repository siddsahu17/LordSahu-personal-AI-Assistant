from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.modules.os_state_engine import OSStateEngine
from app.repositories.goal_repository import GoalRepository
from app.repositories.event_repository import EventRepository
from app.repositories.memory_repository import MemoryRepository
from app.repositories.task_repository import TaskRepository

class ContextBuilder:
    """
    Independent Context Builder collecting Time, Date, OS Phase State, Active Goals,
    Recent Events, Memories, and Pending Tasks into a unified context bundle.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self.os_state_engine = OSStateEngine()
        self.goal_repo = GoalRepository(db)
        self.event_repo = EventRepository(db)
        self.memory_repo = MemoryRepository(db)
        self.task_repo = TaskRepository(db)

    def build_context(self, active_workspace: str = "personal") -> Dict[str, Any]:
        now = datetime.now()
        os_phase = self.os_state_engine.get_current_phase(now)

        goals = self.goal_repo.list_goals(self.user_id, workspace_id=active_workspace)
        recent_events = self.event_repo.query_events(user_id=self.user_id, limit=5)
        memories = self.memory_repo.list_memories(user_id=self.user_id)
        tasks = self.task_repo.list_tasks(user_id=self.user_id, status="PENDING")

        latest_weight = None
        for e in recent_events:
            if e.event_type == "WEIGHT_LOGGED":
                import json
                try:
                    p = json.loads(e.payload) if e.payload else {}
                    latest_weight = p.get("weight_kg") or p.get("weight")
                    if latest_weight:
                        break
                except Exception:
                    pass

        return {
            "current_time_iso": now.isoformat(),
            "current_date_str": now.strftime("%A, %B %d, %Y"),
            "os_phase": os_phase,
            "user_id": self.user_id,
            "active_workspace": active_workspace,
            "current_weight_kg": latest_weight,
            "active_goals": [
                {
                    "id": g.id,
                    "title": g.title,
                    "workspace_id": g.workspace_id,
                    "priority": g.priority,
                    "target_metric": g.target_metric,
                    "target_value": g.target_value
                }
                for g in goals
            ],
            "recent_events": [
                {
                    "id": e.id,
                    "event_type": e.event_type,
                    "workspace_id": e.workspace_id,
                    "created_at": e.created_at.isoformat() if e.created_at else None
                }
                for e in recent_events
            ],
            "pending_tasks": [
                {"id": t.id, "title": t.title, "priority": t.priority}
                for t in tasks[:5]
            ],
            "memories": [
                {"id": m.id, "fact": m.fact, "type": m.memory_type}
                for m in memories[:5]
            ]
        }
