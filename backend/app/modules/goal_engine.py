import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import GoalModel, EventModel
from app.schemas import GoalCreate

class GoalEngine:
    """
    Goal Engine manages user goals and calculates inferred progress dynamically strictly from database events.
    No mock or dummy goals are seeded.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

    def create_goal(self, goal_data: GoalCreate) -> GoalModel:
        db_goal = GoalModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            workspace_id=goal_data.workspace_id,
            title=goal_data.title,
            description=goal_data.description,
            priority=goal_data.priority,
            deadline=goal_data.deadline,
            status=goal_data.status,
            target_metric=goal_data.target_metric,
            target_value=goal_data.target_value,
            manual_progress=goal_data.manual_progress,
            milestones=json.dumps(goal_data.milestones),
            dependencies=json.dumps(goal_data.dependencies),
            tags=json.dumps(goal_data.tags),
            metadata_json=json.dumps(goal_data.metadata_json)
        )
        self.db.add(db_goal)
        self.db.commit()
        self.db.refresh(db_goal)
        return db_goal

    def compute_inferred_progress(self, goal: GoalModel) -> float:
        if goal.manual_progress is not None:
            return min(100.0, max(0.0, float(goal.manual_progress)))

        events = self.db.query(EventModel).filter(EventModel.user_id == self.user_id).all()
        if not events:
            # Check milestone completion if no events
            try:
                m_list = json.loads(goal.milestones)
                if m_list:
                    completed = sum(1 for m in m_list if m.get("completed"))
                    return round((completed / len(m_list)) * 100.0, 1)
            except Exception:
                pass
            return 0.0

        # Calculate progress by hours metric
        if goal.target_metric == "hours" or "study" in goal.title.lower() or "dbms" in goal.title.lower() or "sql" in goal.title.lower():
            total_hours = 0.0
            for e in events:
                if e.event_type == "STUDY_SESSION":
                    try:
                        p = json.loads(e.payload)
                        dur = float(p.get("duration_hours") or p.get("duration") or 0.0)
                        total_hours += dur
                    except Exception:
                        pass
            target = float(goal.target_value or 20.0)
            if target > 0:
                return round(min(100.0, max(0.0, (total_hours / target) * 100.0)), 1)

        # Calculate progress by weight metric
        if goal.target_metric == "kg" or "weight" in goal.title.lower():
            latest_weight = None
            first_weight = None
            weight_events = [e for e in events if e.event_type == "WEIGHT_LOGGED"]
            if weight_events:
                weight_events.sort(key=lambda x: x.created_at)
                try:
                    first_p = json.loads(weight_events[0].payload)
                    first_weight = float(first_p.get("weight_kg") or first_p.get("weight"))
                    latest_p = json.loads(weight_events[-1].payload)
                    latest_weight = float(latest_p.get("weight_kg") or latest_p.get("weight"))
                except Exception:
                    pass

            if first_weight and latest_weight and goal.target_value:
                target_weight = float(goal.target_value)
                total_to_lose = first_weight - target_weight
                lost_so_far = first_weight - latest_weight
                if total_to_lose > 0:
                    return round(min(100.0, max(0.0, (lost_so_far / total_to_lose) * 100.0)), 1)

        # Milestone-based calculation
        try:
            m_list = json.loads(goal.milestones)
            if m_list:
                completed = sum(1 for m in m_list if m.get("completed"))
                return round((completed / len(m_list)) * 100.0, 1)
        except Exception:
            pass

        return 0.0

    def delete_goal(self, goal_identifier: str) -> Optional[str]:
        query = self.db.query(GoalModel).filter(GoalModel.user_id == self.user_id)
        # Match by ID or by title substring
        goal = query.filter(GoalModel.id == goal_identifier).first()
        if not goal:
            goal = query.filter(GoalModel.title.ilike(f"%{goal_identifier}%")).first()

        if goal:
            deleted_title = goal.title
            self.db.delete(goal)
            self.db.commit()
            return deleted_title
        return None

    def list_goals(self, workspace_id: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.db.query(GoalModel).filter(GoalModel.user_id == self.user_id)
        if workspace_id and workspace_id != "all":
            query = query.filter(GoalModel.workspace_id == workspace_id)
        goals = query.all()

        results = []
        for g in goals:
            progress = self.compute_inferred_progress(g)
            try:
                milestones_list = json.loads(g.milestones)
            except Exception:
                milestones_list = []
            try:
                tags_list = json.loads(g.tags)
            except Exception:
                tags_list = []

            results.append({
                "id": g.id,
                "user_id": g.user_id,
                "workspace_id": g.workspace_id,
                "title": g.title,
                "description": g.description,
                "priority": g.priority,
                "deadline": g.deadline.isoformat() if g.deadline else None,
                "status": g.status,
                "target_metric": g.target_metric,
                "target_value": g.target_value,
                "manual_progress": g.manual_progress,
                "inferred_progress": progress,
                "milestones": milestones_list,
                "tags": tags_list,
                "created_at": g.created_at.isoformat() if g.created_at else None
            })
        return results
