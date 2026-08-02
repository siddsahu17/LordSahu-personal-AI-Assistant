import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.workspaces.base_workspace import BaseWorkspaceModule
from app.tools.base_tool import BaseTool
from app.skills.personal_skill import PersonalSkill
from app.repositories.event_repository import EventRepository

class PersonalWorkspace(BaseWorkspaceModule):
    workspace_id = "personal"
    workspace_name = "Personal Intelligence Module"

    def get_skill_tools(self) -> List[BaseTool]:
        return PersonalSkill().get_tools()

    def get_analytics_overview(self, db: Session, user_id: str = "default_user") -> Dict[str, Any]:
        repo = EventRepository(db)
        events = repo.query_events(user_id=user_id, workspace_id="personal", limit=50)

        journals = []
        moods = []

        for e in events:
            if not e.payload:
                continue
            try:
                p = json.loads(e.payload)
            except Exception:
                continue

            if e.event_type == "JOURNAL_ENTRY":
                journals.append(p.get("text"))
            elif e.event_type == "MOOD_LOGGED":
                moods.append(p.get("mood"))

        return {
            "total_journal_entries": len(journals),
            "recent_reflections": journals[:5],
            "latest_mood": moods[0] if moods else "Positive",
            "coaching_insights": self.get_coaching_insights(db, user_id)
        }

    def get_coaching_insights(self, db: Session, user_id: str = "default_user") -> List[str]:
        return ["🌿 Personal Life Journal. Share daily thoughts or reflections anytime."]
