import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import GoalModel, EventModel
from app.schemas import GoalCreate

DEFAULT_GOALS = [
    {
        "title": "DBMS & SQL Joins Mastery",
        "workspace_id": "learning",
        "description": "Complete DBMS assignments, master SQL joins, and achieve exam readiness.",
        "priority": "HIGH",
        "target_metric": "hours",
        "target_value": 20.0,
        "tags": ["learning", "dbms", "sql", "college"],
        "milestones": [
            {"id": "m1", "title": "Complete Relational Algebra", "completed": True, "target": 5.0, "current": 5.0},
            {"id": "m2", "title": "Master SQL Joins & Subqueries", "completed": False, "target": 10.0, "current": 4.5},
            {"id": "m3", "title": "DBMS Normalization & Indexing", "completed": False, "target": 5.0, "current": 0.0}
        ]
    },
    {
        "title": "Weight Loss Target (80 kg)",
        "workspace_id": "fitness",
        "description": "Progressively drop bodyweight from ~99 kg down to 80 kg target.",
        "priority": "HIGH",
        "target_metric": "kg",
        "target_value": 80.0,
        "tags": ["health", "weight", "fitness"],
        "milestones": [
            {"id": "m1", "title": "Reach 95 kg", "completed": False, "target": 95.0, "current": 96.8},
            {"id": "m2", "title": "Reach 90 kg", "completed": False, "target": 90.0, "current": 96.8},
            {"id": "m3", "title": "Reach 85 kg", "completed": False, "target": 85.0, "current": 96.8},
            {"id": "m4", "title": "Reach 80 kg", "completed": False, "target": 80.0, "current": 96.8}
        ]
    },
    {
        "title": "Build LordSahu AI OS V0.1",
        "workspace_id": "projects",
        "description": "Architect and deploy LordSahu AI Personal Operating System.",
        "priority": "HIGH",
        "target_metric": "tasks",
        "target_value": 10.0,
        "tags": ["projects", "ai", "lordsahu"],
        "milestones": [
            {"id": "m1", "title": "Event Store & Core Intelligence Layer", "completed": True, "target": 1.0, "current": 1.0},
            {"id": "m2", "title": "Voice Engine & Mission Control UI", "completed": True, "target": 1.0, "current": 1.0}
        ]
    }
]

class GoalEngine:
    """
    Goal Engine manages goals and calculates inferred progress dynamically from events.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self._ensure_defaults()

    def _ensure_defaults(self):
        count = self.db.query(GoalModel).filter(GoalModel.user_id == self.user_id).count()
        if count == 0:
            for g in DEFAULT_GOALS:
                db_goal = GoalModel(
                    id=str(uuid.uuid4()),
                    user_id=self.user_id,
                    workspace_id=g["workspace_id"],
                    title=g["title"],
                    description=g["description"],
                    priority=g["priority"],
                    target_metric=g["target_metric"],
                    target_value=g["target_value"],
                    tags=json.dumps(g["tags"]),
                    milestones=json.dumps(g["milestones"])
                )
                self.db.add(db_goal)
            self.db.commit()

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

        # Inferred progress calculation from Events
        events = self.db.query(EventModel).filter(EventModel.user_id == self.user_id).all()
        
        if goal.workspace_id == "fitness" or "weight" in goal.title.lower():
            # Calculate weight loss progress
            latest_weight = None
            for e in sorted(events, key=lambda x: x.created_at, reverse=True):
                if e.event_type == "WEIGHT_LOGGED":
                    try:
                        p = json.loads(e.payload)
                        latest_weight = p.get("weight_kg") or p.get("weight")
                        if latest_weight:
                            break
                    except Exception:
                        pass
            if latest_weight and goal.target_value:
                start_weight = 99.0  # initial reference weight
                target_weight = float(goal.target_value)
                total_to_lose = start_weight - target_weight
                lost_so_far = start_weight - float(latest_weight)
                if total_to_lose > 0:
                    pct = (lost_so_far / total_to_lose) * 100.0
                    return round(min(100.0, max(0.0, pct)), 1)
            return 25.0  # fallback baseline

        if goal.target_metric == "hours" or "dbms" in goal.title.lower():
            total_hours = 0.0
            for e in events:
                if e.event_type == "STUDY_SESSION":
                    try:
                        p = json.loads(e.payload)
                        dur = float(p.get("duration_hours") or p.get("duration") or 0.0)
                        total_hours += dur
                    except Exception:
                        pass
            # Include default completed baseline hours (e.g. 8.5h out of 20h = 42.5%)
            total_hours += 8.5
            target = float(goal.target_value or 20.0)
            if target > 0:
                pct = (total_hours / target) * 100.0
                return round(min(100.0, max(0.0, pct)), 1)

        # Default milestone-based calculation
        try:
            m_list = json.loads(goal.milestones)
            if m_list:
                completed = sum(1 for m in m_list if m.get("completed"))
                return round((completed / len(m_list)) * 100.0, 1)
        except Exception:
            pass

        return 50.0

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
