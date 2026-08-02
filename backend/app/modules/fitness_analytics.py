import json
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.repositories.event_repository import EventRepository

class FitnessAnalyticsEngine:
    """
    Derived Fitness Analytics Engine for LordSahu Fitness Intelligence Module.
    Generates real-time derived metrics & AI coaching insights strictly from immutable Fitness Events.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self.repo = EventRepository(db)

    def compute_fitness_overview(self) -> Dict[str, Any]:
        events = self.repo.query_events(user_id=self.user_id, workspace_id="fitness", limit=100)

        weights = []
        workouts = []
        sports = []
        water_today = 0.0
        sleep_records = []
        prs = []

        now = datetime.now(timezone.utc)
        today_str = now.strftime("%Y-%m-%d")

        for e in events:
            if not e.payload:
                continue
            try:
                p = json.loads(e.payload)
            except Exception:
                continue

            c_date = e.created_at.strftime("%Y-%m-%d") if e.created_at else today_str

            if e.event_type == "WEIGHT_LOGGED":
                w_val = p.get("weight_kg") or p.get("weight")
                if w_val:
                    weights.append({"weight_kg": float(w_val), "date": c_date})

            elif e.event_type in ("WORKOUT_SESSION", "WORKOUT_COMPLETED"):
                workouts.append({
                    "id": e.id,
                    "workout_type": p.get("workout_type", "Workout"),
                    "volume_kg": float(p.get("total_volume_kg") or 0.0),
                    "exercises": p.get("exercises", []),
                    "date": c_date
                })

            elif e.event_type == "SPORT_COMPLETED":
                sports.append({
                    "sport_name": p.get("sport_name", "Sport"),
                    "duration_mins": float(p.get("duration_mins") or 60.0),
                    "intensity": p.get("intensity", "Moderate"),
                    "date": c_date
                })

            elif e.event_type == "WATER_LOGGED" and c_date == today_str:
                water_today += float(p.get("liters") or 0.0)

            elif e.event_type == "SLEEP_LOGGED":
                sleep_records.append(float(p.get("hours") or 7.0))

            elif e.event_type == "PR_ACHIEVED":
                prs.append({
                    "exercise": p.get("exercise_name"),
                    "weight_kg": p.get("weight_kg"),
                    "date": c_date
                })

        # Calculations
        latest_weight = weights[0]["weight_kg"] if weights else None
        weight_moving_avg = round(sum(w["weight_kg"] for w in weights[:7]) / len(weights[:7]), 1) if weights else None
        weekly_volume = sum(w["volume_kg"] for w in workouts)
        avg_sleep = round(sum(sleep_records) / len(sleep_records), 1) if sleep_records else 7.5

        # AI Coaching Insights
        insights = []
        if workouts:
            last_w_type = workouts[0]["workout_type"]
            insights.append(f"💪 Last completed workout was **{last_w_type}** with total volume of **{workouts[0]['volume_kg']}kg**.")
        else:
            insights.append("💪 No workouts logged yet. Start a session anytime e.g. 'I completed chest day'!")

        if latest_weight:
            insights.append(f"⚖️ Current recorded body weight is **{latest_weight} kg** (7-day average: {weight_moving_avg} kg).")

        if prs:
            insights.append(f"🏆 Recent PR: **{prs[0]['exercise']}** @ **{prs[0]['weight_kg']} kg**!")

        return {
            "latest_weight_kg": latest_weight,
            "weight_moving_avg_7d": weight_moving_avg,
            "weight_history": weights[:10],
            "weekly_workout_volume_kg": weekly_volume,
            "workout_count": len(workouts),
            "recent_workouts": workouts[:5],
            "sports_count": len(sports),
            "recent_sports": sports[:5],
            "water_today_liters": round(water_today, 1),
            "avg_sleep_hours": avg_sleep,
            "personal_records": prs[:5],
            "coaching_insights": insights
        }
