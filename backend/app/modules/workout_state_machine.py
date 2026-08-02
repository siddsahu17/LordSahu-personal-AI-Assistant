import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.repositories.event_repository import EventRepository
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class WorkoutStateMachine:
    """
    Workout Conversation State Machine for LordSahu Fitness Intelligence Module.
    Manages multi-turn workout logging sessions (IDLE -> WORKOUT_STARTED -> COLLECTING_EXERCISES -> WORKOUT_COMPLETED).
    Includes Smart Conversation Pre-Fill from previous workout sessions.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorkoutStateMachine, cls).__new__(cls)
            cls._instance.active_sessions: Dict[str, Dict[str, Any]] = {}
        return cls._instance

    def get_session_state(self, user_id: str = "default_user") -> Dict[str, Any]:
        return self.active_sessions.get(user_id, {"state": "IDLE", "exercises": []})

    def start_workout(self, user_id: str, workout_type: str, db: Session) -> Dict[str, Any]:
        last_config = self.get_last_workout_config(user_id, workout_type, db)
        session = {
            "state": "WORKOUT_STARTED",
            "workout_type": workout_type,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "exercises": [],
            "last_config": last_config
        }
        self.active_sessions[user_id] = session

        reply = f"Workout session '{workout_type}' started!"
        if last_config and last_config.get("exercises"):
            ex_list = ", ".join([e["name"] for e in last_config["exercises"]])
            reply += f"\n💡 Smart Pre-Fill: Your last {workout_type} included: **{ex_list}**.\nTell me your exercises one by one (e.g., 'Bench Press 20 kg 3 sets 12 reps'). Say 'Workout completed' when finished."
        else:
            reply += "\nTell me your exercises one by one (e.g., 'Bench Press 20 kg 3 sets 12 reps'). Say 'Workout completed' when finished."

        return {"status": "started", "reply": reply, "state": session["state"]}

    def add_exercise(self, user_id: str, name: str, weight_kg: float, sets: int, reps: int, notes: str = "") -> Dict[str, Any]:
        session = self.active_sessions.get(user_id)
        if not session or session["state"] == "IDLE":
            session = {
                "state": "WORKOUT_STARTED",
                "workout_type": "General Workout",
                "start_time": datetime.now(timezone.utc).isoformat(),
                "exercises": [],
                "last_config": None
            }
            self.active_sessions[user_id] = session

        exercise_entry = {
            "name": name,
            "weight_kg": weight_kg,
            "sets": sets,
            "reps": reps,
            "volume": weight_kg * sets * reps,
            "notes": notes
        }
        session["exercises"].append(exercise_entry)
        session["state"] = "COLLECTING_EXERCISES"

        return {
            "status": "exercise_added",
            "exercise": exercise_entry,
            "total_exercises": len(session["exercises"]),
            "reply": f"Added **{name}**: {weight_kg}kg x {sets} sets x {reps} reps (Volume: {exercise_entry['volume']}kg). Add next exercise or say 'Workout completed'."
        }

    def finalize_workout(self, user_id: str, db: Session) -> Dict[str, Any]:
        session = self.active_sessions.get(user_id)
        if not session or not session.get("exercises"):
            self.active_sessions[user_id] = {"state": "IDLE", "exercises": []}
            return {
                "status": "empty",
                "reply": "No exercises were recorded in this workout session.",
                "total_volume": 0.0
            }

        workout_type = session.get("workout_type", "Workout")
        exercises = session["exercises"]
        total_volume = sum(e["volume"] for e in exercises)
        est_duration = max(20, len(exercises) * 12)

        evt_engine = EventEngine(db, user_id)
        workout_evt = evt_engine.create_event(EventCreate(
            workspace_id="fitness",
            source="chat_text",
            event_type="WORKOUT_SESSION",
            intent="LOG_WORKOUT",
            payload={
                "workout_type": workout_type,
                "total_volume_kg": total_volume,
                "estimated_duration_mins": est_duration,
                "exercise_count": len(exercises),
                "exercises": exercises
            }
        ))

        # Reset State to IDLE
        self.active_sessions[user_id] = {"state": "IDLE", "exercises": []}

        summary_lines = [f"🏋️ **{workout_type} Completed!**"]
        summary_lines.append(f"• Total Volume: **{total_volume} kg** across {len(exercises)} exercises.")
        summary_lines.append(f"• Estimated Duration: ~{est_duration} mins.")
        summary_lines.append("\nExercises Recorded:")
        for ex in exercises:
            summary_lines.append(f"  - **{ex['name']}**: {ex['weight_kg']}kg x {ex['sets']}s x {ex['reps']}r ({ex['volume']}kg volume)")

        return {
            "status": "finalized",
            "workout_event_id": workout_evt.id,
            "total_volume": total_volume,
            "reply": "\n".join(summary_lines)
        }

    def get_last_workout_config(self, user_id: str, workout_type: str, db: Session) -> Optional[Dict[str, Any]]:
        evt_repo = EventRepository(db)
        events = evt_repo.query_events(user_id=user_id, workspace_id="fitness", event_type="WORKOUT_SESSION", limit=10)
        for e in events:
            if e.payload:
                try:
                    p = json.loads(e.payload)
                    if p.get("workout_type", "").lower() == workout_type.lower():
                        return p
                except Exception:
                    pass
        return None

# Global Singleton
workout_state_machine = WorkoutStateMachine()
