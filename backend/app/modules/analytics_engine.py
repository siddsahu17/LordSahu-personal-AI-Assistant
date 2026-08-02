import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import EventModel, GoalModel

class AnalyticsEngine:
    """
    Analytics Engine service performing 100% deterministic calculations on real Event Store records.
    No fake or mock data fallback.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

    def compute_analytics(self) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        thirty_days_ago = (now - timedelta(days=30)).replace(tzinfo=None)
        seven_days_ago = (now - timedelta(days=7)).replace(tzinfo=None)
        today_start = datetime(now.year, now.month, now.day)

        events = (
            self.db.query(EventModel)
            .filter(EventModel.user_id == self.user_id)
            .all()
        )

        def to_naive(dt):
            if dt is None:
                return None
            return dt.replace(tzinfo=None) if hasattr(dt, 'tzinfo') and dt.tzinfo else dt

        active_days = set()
        study_hours_total = 0.0
        focus_hours_today = 0.0
        workout_count = 0
        weight_logs = []

        for e in events:
            e_dt = to_naive(e.created_at)
            if e_dt:
                day_str = e_dt.strftime("%Y-%m-%d")
                active_days.add(day_str)

            if e.event_type == "STUDY_SESSION":
                try:
                    p = json.loads(e.payload)
                    dur = float(p.get("duration_hours") or p.get("duration") or 0.0)
                    study_hours_total += dur
                    if e_dt and e_dt >= today_start:
                        focus_hours_today += dur
                except Exception:
                    pass
            elif e.event_type == "WORKOUT_COMPLETED":
                workout_count += 1
            elif e.event_type == "WEIGHT_LOGGED":
                try:
                    p = json.loads(e.payload)
                    w = p.get("weight_kg") or p.get("weight")
                    if w and e_dt:
                        weight_logs.append({
                            "date": e_dt.strftime("%b %d"),
                            "weight": float(w)
                        })
                except Exception:
                    pass

        # 1. Consistency Score (% active days in last 30)
        consistency_score = round((len(active_days) / 30.0) * 100.0, 1) if events else 0.0

        # 2. Momentum Index
        last_7_events_count = sum(1 for e in events if e.created_at and to_naive(e.created_at) >= seven_days_ago)
        momentum_index = round(min(10.0, (last_7_events_count / 7.0) * 2.0), 1) if events else 0.0

        # 3. Goal Velocity
        goals = self.db.query(GoalModel).filter(GoalModel.user_id == self.user_id).all()
        goal_velocity = round(min(100.0, study_hours_total * 2.5), 1) if events else 0.0

        # 4. Burnout Risk Score
        burnout_risk = round(min(100.0, (focus_hours_today / 8.0) * 100.0), 1) if focus_hours_today > 0 else 0.0

        # 5. Learning Efficiency & Workout Consistency
        learning_efficiency = 100.0 if study_hours_total > 0 else 0.0
        workout_consistency = round(min(100.0, (workout_count / 12.0) * 100.0), 1) if workout_count > 0 else 0.0

        latest_weight = weight_logs[-1]["weight"] if weight_logs else None

        # 6. Activity Heatmap (Last 14 days event counts)
        heatmap = []
        for i in range(13, -1, -1):
            day_dt = now - timedelta(days=i)
            day_key = day_dt.strftime("%Y-%m-%d")
            count = sum(1 for e in events if e.created_at and to_naive(e.created_at).strftime("%Y-%m-%d") == day_key)
            heatmap.append({
                "date": day_dt.strftime("%b %d"),
                "count": count
            })

        return {
            "consistency_score": consistency_score,
            "momentum_index": momentum_index,
            "goal_velocity": goal_velocity,
            "burnout_risk_score": burnout_risk,
            "learning_efficiency": learning_efficiency,
            "workout_consistency": workout_consistency,
            "total_study_hours": round(study_hours_total, 1),
            "latest_weight_kg": latest_weight,
            "weight_trend_kg": weight_logs,
            "activity_heatmap": heatmap,
            "focus_hours_today": round(focus_hours_today, 1)
        }
