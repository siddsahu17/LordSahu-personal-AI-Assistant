from typing import Dict, Any
from sqlalchemy.orm import Session
from app.modules.analytics_engine import AnalyticsEngine

class ReportGenerator:
    """
    Report Generator produces reflections based 100% on real Event Store records in SQLite.
    No mock data.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self.analytics = AnalyticsEngine(db, user_id)

    def generate_report(self, timeframe: str = "weekly") -> Dict[str, Any]:
        metrics = self.analytics.compute_analytics()
        has_events = metrics.get("total_study_hours", 0) > 0 or metrics.get("latest_weight_kg") is not None or metrics.get("consistency_score", 0) > 0

        if not has_events:
            return {
                "timeframe": f"{timeframe.capitalize()} Report",
                "period": f"Current {timeframe.capitalize()}",
                "reflection": "No life events logged yet in your Event Store. Talk to LordSahu or record an event to generate your first AI reflection report!",
                "strengths": ["System ready to log events"],
                "weaknesses": ["No events recorded yet"],
                "recommendations": ["Log your first weight, study session, or workout via LordSahu Chat."],
                "metrics": metrics
            }

        weight_str = f"Current weight: {metrics['latest_weight_kg']} kg." if metrics.get('latest_weight_kg') else ""
        study_str = f"Logged {metrics['total_study_hours']} study hours." if metrics.get('total_study_hours') else ""

        return {
            "timeframe": f"{timeframe.capitalize()} Reflection",
            "period": f"Past {timeframe}",
            "reflection": f"Report generated from Event Store. Consistency Score: {metrics['consistency_score']}%. {study_str} {weight_str}",
            "strengths": [
                f"Consistency score currently at {metrics['consistency_score']}%",
                f"Total study hours logged: {metrics['total_study_hours']}h"
            ],
            "weaknesses": [
                "Track workouts consistently to boost health momentum" if metrics.get('workout_consistency', 0) < 50 else "Maintain current rest balance"
            ],
            "recommendations": [
                "Continue logging events daily to keep your AI Personal Operating System synchronized."
            ],
            "metrics": metrics
        }
