import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import EventModel, GoalModel, MemoryModel, TaskModel, ChatMessageModel

class ContextEngine:
    """
    Context Engine builds the full real-time user state bundle BEFORE any AI intent/entity parsing or prompt generation.
    """
    def __init__(self, db: Session, user_id: str = "default_user", workspace_id: str = "personal"):
        self.db = db
        self.user_id = user_id
        self.workspace_id = workspace_id

    def build_context(self) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        current_time_iso = now.isoformat()
        current_date_str = now.strftime("%A, %B %d, %Y")

        # Fetch latest weight log
        latest_weight_event = (
            self.db.query(EventModel)
            .filter(EventModel.user_id == self.user_id, EventModel.event_type == "WEIGHT_LOGGED")
            .order_by(EventModel.created_at.desc())
            .first()
        )
        current_weight = None
        if latest_weight_event:
            try:
                payload = json.loads(latest_weight_event.payload)
                current_weight = payload.get("weight_kg") or payload.get("weight")
            except Exception:
                pass

        # Fetch active goals
        active_goals = (
            self.db.query(GoalModel)
            .filter(GoalModel.user_id == self.user_id, GoalModel.status != "COMPLETED")
            .all()
        )
        goals_summary = [
            {
                "id": g.id,
                "title": g.title,
                "workspace_id": g.workspace_id,
                "priority": g.priority,
                "target_metric": g.target_metric,
                "target_value": g.target_value
            }
            for g in active_goals
        ]

        # Fetch today's events
        start_of_day = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        todays_events = (
            self.db.query(EventModel)
            .filter(EventModel.user_id == self.user_id, EventModel.created_at >= start_of_day)
            .order_by(EventModel.created_at.asc())
            .all()
        )
        events_summary = []
        for e in todays_events:
            try:
                p = json.loads(e.payload)
            except Exception:
                p = {}
            events_summary.append({
                "id": e.id,
                "event_type": e.event_type,
                "workspace_id": e.workspace_id,
                "payload": p,
                "time": e.created_at.strftime("%H:%M")
            })

        # Fetch pending tasks
        pending_tasks = (
            self.db.query(TaskModel)
            .filter(TaskModel.user_id == self.user_id, TaskModel.status == "PENDING")
            .order_by(TaskModel.created_at.desc())
            .limit(5)
            .all()
        )
        tasks_summary = [{"id": t.id, "title": t.title, "priority": t.priority} for t in pending_tasks]

        # Fetch recent chat message window (last 5)
        recent_chats = (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.user_id == self.user_id)
            .order_by(ChatMessageModel.created_at.desc())
            .limit(5)
            .all()
        )
        recent_chats.reverse()
        chat_history = [{"sender": c.sender, "text": c.text, "mode": c.mode} for c in recent_chats]

        return {
            "current_time_iso": current_time_iso,
            "current_date_str": current_date_str,
            "user_id": self.user_id,
            "active_workspace": self.workspace_id,
            "current_weight_kg": current_weight,
            "active_goals": goals_summary,
            "todays_events": events_summary,
            "pending_tasks": tasks_summary,
            "recent_chat_history": chat_history
        }
