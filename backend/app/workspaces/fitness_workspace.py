from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.workspaces.base_workspace import BaseWorkspaceModule
from app.tools.base_tool import BaseTool
from app.skills.fitness_skill import FitnessSkill
from app.modules.fitness_analytics import FitnessAnalyticsEngine

class FitnessWorkspace(BaseWorkspaceModule):
    workspace_id = "fitness"
    workspace_name = "Fitness Intelligence Module (FIM)"

    def get_skill_tools(self) -> List[BaseTool]:
        return FitnessSkill().get_tools()

    def get_analytics_overview(self, db: Session, user_id: str = "default_user") -> Dict[str, Any]:
        engine = FitnessAnalyticsEngine(db, user_id)
        return engine.compute_fitness_overview()

    def get_coaching_insights(self, db: Session, user_id: str = "default_user") -> List[str]:
        engine = FitnessAnalyticsEngine(db, user_id)
        ov = engine.compute_fitness_overview()
        return ov.get("coaching_insights", [])
