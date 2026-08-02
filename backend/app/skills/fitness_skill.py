from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.fitness_commands import (
    LogWeightCommand, LogWorkoutCommand, LogSportCommand,
    LogMealCommand, LogWaterCommand, LogSleepCommand, LogPRCommand
)

class LogWeightTool(BaseTool):
    name = "log_weight"
    description = "Log body weight in kg into Fitness Journal."
    category = "fitness"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogWeightCommand(db, user_id)
        return cmd.execute(params)

class LogWorkoutTool(BaseTool):
    name = "log_workout"
    description = "Log workout session into Fitness Journal."
    category = "fitness"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogWorkoutCommand(db, user_id)
        return cmd.execute(params)

class LogSportTool(BaseTool):
    name = "log_sport"
    description = "Log sports activity (Football, Basketball, Running, Cycling, Swimming, Tennis, Yoga)."
    category = "fitness"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogSportCommand(db, user_id)
        return cmd.execute(params)

class LogMealTool(BaseTool):
    name = "log_meal"
    description = "Log meal & nutrition into Fitness Journal."
    category = "fitness"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogMealCommand(db, user_id)
        return cmd.execute(params)

class LogWaterTool(BaseTool):
    name = "log_water"
    description = "Log daily hydration water intake in liters into Fitness Journal."
    category = "fitness"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogWaterCommand(db, user_id)
        return cmd.execute(params)

class LogSleepTool(BaseTool):
    name = "log_sleep"
    description = "Log sleep duration and quality score into Fitness Journal."
    category = "fitness"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogSleepCommand(db, user_id)
        return cmd.execute(params)

class LogPRTool(BaseTool):
    name = "log_pr"
    description = "Log Personal Record achievement in exercise weight."
    category = "fitness"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogPRCommand(db, user_id)
        return cmd.execute(params)

class FitnessSkill(BaseSkill):
    name = "fitness_skill"
    description = "Complete AI Fitness Intelligence Module (weight, workouts, sports, nutrition, water, sleep, PRs)."

    def get_tools(self) -> List[BaseTool]:
        return [
            LogWeightTool(), LogWorkoutTool(), LogSportTool(),
            LogMealTool(), LogWaterTool(), LogSleepTool(), LogPRTool()
        ]
