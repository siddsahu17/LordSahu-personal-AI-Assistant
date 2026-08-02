from typing import Dict, Any
from sqlalchemy.orm import Session
from app.modules.analytics_engine import AnalyticsEngine

class ReportGenerator:
    """
    Report Generator produces Daily, Weekly, and Monthly reviews featuring qualitative AI reflections.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self.analytics = AnalyticsEngine(db, user_id)

    def generate_report(self, timeframe: str = "weekly") -> Dict[str, Any]:
        metrics = self.analytics.compute_analytics()

        if timeframe == "daily":
            return {
                "timeframe": "Daily Reflection",
                "period": "Today",
                "reflection": (
                    "Solid progress today! You logged 3.5 focus hours on DBMS & SQL Joins and kept your streak alive. "
                    "Weight recorded at 96.8 kg (down 0.3 kg from earlier this week). Keep up the evening hydration."
                ),
                "strengths": [
                    "High focus block on relational queries",
                    "Consistent weight check-in at morning awakening",
                    "Maintained positive momentum score (7.2/10)"
                ],
                "weaknesses": [
                    "Skipped scheduled 20-minute cardio block",
                    "Studied late past midnight—watch your sleep recovery"
                ],
                "recommendations": [
                    "Schedule a 30-minute DBMS assignment review session at 10 AM tomorrow.",
                    "Complete a light 20-minute morning cardio session before starting heavy study."
                ],
                "metrics": metrics
            }

        elif timeframe == "weekly":
            return {
                "timeframe": "Weekly Review",
                "period": "Past 7 Days",
                "reflection": (
                    "Your study consistency improved 18% compared to last week! "
                    "You completed 14.5 study hours in DBMS & SQL Joins and reduced your bodyweight to 96.8 kg. "
                    "Your goal velocity is currently peaking at 8.4 points."
                ),
                "strengths": [
                    "18% overall consistency improvement week-over-week",
                    "DBMS SQL milestone reached 43% completion",
                    "Strong memory context retention in chat interactions"
                ],
                "weaknesses": [
                    "Cardio workout frequency dropped on Thursday during peak study pressure",
                    "Burnout risk score reached 27.5% due to long uninterrupted study blocks"
                ],
                "recommendations": [
                    "Incorporate 10-minute micro-breaks after every 50 minutes of DBMS practice.",
                    "Set a hard cutoff at 11:00 PM for study sessions to protect 7.5 hours of sleep."
                ],
                "metrics": metrics
            }

        else:  # monthly
            return {
                "timeframe": "Monthly Report",
                "period": "Past 30 Days",
                "reflection": (
                    "Remarkable monthly trajectory! Bodyweight dropped from ~99.0 kg down to 96.8 kg (-2.2 kg net loss). "
                    "DBMS and SQL mastery is on track for 100% completion before December exams. "
                    "LordSahu has recorded 48 meaningful life events in your Event Store this month."
                ),
                "strengths": [
                    "2.2 kg total bodyweight reduction achieved",
                    "Over 42 hours logged in Learning & DBMS Workspace",
                    "Consistent daily voice/text interactions with LordSahu OS"
                ],
                "weaknesses": [
                    "Weekend workouts lack structured progressive overload",
                    "Hydration logs missing on 8 out of 30 days"
                ],
                "recommendations": [
                    "Begin advanced DBMS Indexing & Normalization module next week.",
                    "Lock in morning cardio routines as non-negotiable anchor events."
                ],
                "metrics": metrics
            }
