import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.workspaces.base_workspace import BaseWorkspaceModule
from app.tools.base_tool import BaseTool
from app.skills.project_skill import ProjectSkill
from app.repositories.event_repository import EventRepository

class ProjectsWorkspace(BaseWorkspaceModule):
    workspace_id = "projects"
    workspace_name = "Project Intelligence Module"

    def get_skill_tools(self) -> List[BaseTool]:
        return ProjectSkill().get_tools()

    def get_analytics_overview(self, db: Session, user_id: str = "default_user") -> Dict[str, Any]:
        repo = EventRepository(db)
        events = repo.query_events(user_id=user_id, workspace_id="projects", limit=50)

        features = []
        bugs = []

        for e in events:
            if not e.payload:
                continue
            try:
                p = json.loads(e.payload)
            except Exception:
                continue

            if e.event_type == "FEATURE_BUILT":
                features.append(p.get("feature_name"))
            elif e.event_type == "BUG_FIXED":
                bugs.append(p.get("bug_summary"))

        return {
            "features_implemented": len(features),
            "recent_features": features[:5],
            "bugs_resolved": len(bugs),
            "recent_bugs": bugs[:5],
            "coaching_insights": self.get_coaching_insights(db, user_id)
        }

    def get_coaching_insights(self, db: Session, user_id: str = "default_user") -> List[str]:
        return ["🛠️ Software Project Journal Active. High development velocity!"]
