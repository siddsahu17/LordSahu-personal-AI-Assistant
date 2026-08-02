import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.workspaces.base_workspace import BaseWorkspaceModule
from app.tools.base_tool import BaseTool
from app.skills.learning_skill import LearningSkill
from app.repositories.event_repository import EventRepository

class LearningWorkspace(BaseWorkspaceModule):
    workspace_id = "learning"
    workspace_name = "Learning Intelligence Module (LIM)"

    def get_skill_tools(self) -> List[BaseTool]:
        return LearningSkill().get_tools()

    def get_analytics_overview(self, db: Session, user_id: str = "default_user") -> Dict[str, Any]:
        repo = EventRepository(db)
        events = repo.query_events(user_id=user_id, workspace_id="learning", limit=50)

        concepts = []
        problems = []
        total_study_hours = 0.0

        for e in events:
            if not e.payload:
                continue
            try:
                p = json.loads(e.payload)
            except Exception:
                continue

            if e.event_type == "CONCEPT_LEARNED":
                concepts.append(p.get("concept_name", "Concept"))
            elif e.event_type == "PROBLEM_SOLVED":
                problems.append({"title": p.get("problem_title"), "difficulty": p.get("difficulty", "Medium")})
            elif e.event_type == "STUDY_SESSION":
                total_study_hours += float(p.get("duration_hours") or 1.0)

        return {
            "total_concepts_learned": len(concepts),
            "concepts": concepts[:5],
            "total_problems_solved": len(problems),
            "problems": problems[:5],
            "total_study_hours": round(total_study_hours, 1),
            "coaching_insights": self.get_coaching_insights(db, user_id)
        }

    def get_coaching_insights(self, db: Session, user_id: str = "default_user") -> List[str]:
        repo = EventRepository(db)
        events = repo.query_events(user_id=user_id, workspace_id="learning", limit=10)
        if not events:
            return ["📘 No learning events logged yet. Tell LordSahu: 'Today I learned Docker Compose'."]
        return [f"🧠 Great progress! Registered {len(events)} recent learning achievements in your Learning Graph."]
