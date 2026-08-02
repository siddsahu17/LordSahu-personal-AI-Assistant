from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.repositories.memory_repository import MemoryRepository
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class LogWeightCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        weight_kg = float(params.get("weight_kg") or 0.0)
        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="fitness",
            source="chat_text",
            event_type="WEIGHT_LOGGED",
            intent="LOG_WEIGHT",
            payload={"weight_kg": weight_kg}
        ))

        mem_repo = MemoryRepository(self.db)
        mem_repo.add(mem_repo.model_cls(
            user_id=self.user_id,
            workspace_id="fitness",
            memory_type="FACT",
            category="fitness",
            fact=f"Current body weight recorded as {weight_kg} kg"
        ))
        return {
            "status": "success",
            "weight_kg": weight_kg,
            "event_id": evt.id,
            "message": f"Logged body weight {weight_kg} kg into Fitness Journal."
        }

class LogWorkoutCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        w_type = params.get("workout_type") or "Cardio & Workout"
        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="fitness",
            source="chat_text",
            event_type="WORKOUT_COMPLETED",
            intent="LOG_WORKOUT",
            payload={"workout_type": w_type}
        ))
        return {"status": "success", "workout_type": w_type, "event_id": evt.id, "message": f"Logged '{w_type}' session into Fitness Journal."}

class LogSportCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        sport_name = params.get("sport_name") or "Sports"
        duration_mins = float(params.get("duration_mins") or 60.0)
        intensity = params.get("intensity") or "Moderate"

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="fitness",
            source="chat_text",
            event_type="SPORT_COMPLETED",
            intent="LOG_SPORT",
            payload={"sport_name": sport_name, "duration_mins": duration_mins, "intensity": intensity}
        ))
        return {
            "status": "success",
            "sport_name": sport_name,
            "duration_mins": duration_mins,
            "event_id": evt.id,
            "message": f"Logged {duration_mins} mins of {sport_name} ({intensity} intensity) into Fitness Journal."
        }

class LogMealCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        meal_type = params.get("meal_type") or "Meal"
        description = params.get("description") or "Food items"

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="fitness",
            source="chat_text",
            event_type="MEAL_LOGGED",
            intent="LOG_MEAL",
            payload={"meal_type": meal_type, "description": description}
        ))
        return {
            "status": "success",
            "meal_type": meal_type,
            "event_id": evt.id,
            "message": f"Logged {meal_type} ({description}) into Fitness Journal."
        }

class LogWaterCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        liters = float(params.get("liters") or 1.0)
        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="fitness",
            source="chat_text",
            event_type="WATER_LOGGED",
            intent="LOG_WATER",
            payload={"liters": liters}
        ))
        return {
            "status": "success",
            "liters": liters,
            "event_id": evt.id,
            "message": f"Logged {liters}L of water into Fitness Journal."
        }

class LogSleepCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        hours = float(params.get("hours") or 7.0)
        quality = params.get("quality") or "Good"

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="fitness",
            source="chat_text",
            event_type="SLEEP_LOGGED",
            intent="LOG_SLEEP",
            payload={"hours": hours, "quality": quality}
        ))
        return {
            "status": "success",
            "hours": hours,
            "event_id": evt.id,
            "message": f"Logged {hours} hours of sleep ({quality} quality) into Fitness Journal."
        }

class LogPRCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        exercise_name = params.get("exercise_name") or "Bench Press"
        weight_kg = float(params.get("weight_kg") or 0.0)

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="fitness",
            source="chat_text",
            event_type="PR_ACHIEVED",
            intent="LOG_PR",
            payload={"exercise_name": exercise_name, "weight_kg": weight_kg}
        ))
        return {
            "status": "success",
            "exercise_name": exercise_name,
            "weight_kg": weight_kg,
            "event_id": evt.id,
            "message": f"🏆 Personal Record Celebrated: {exercise_name} @ {weight_kg}kg!"
        }
