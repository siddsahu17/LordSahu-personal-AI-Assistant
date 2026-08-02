import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.workspaces.base_workspace import BaseWorkspaceModule
from app.tools.base_tool import BaseTool
from app.skills.career_skill import CareerSkill
from app.repositories.event_repository import EventRepository

class CareerWorkspace(BaseWorkspaceModule):
    workspace_id = "career"
    workspace_name = "Career Intelligence Module (CIM)"

    def get_skill_tools(self) -> List[BaseTool]:
        return CareerSkill().get_tools()

    def get_analytics_overview(self, db: Session, user_id: str = "default_user") -> Dict[str, Any]:
        repo = EventRepository(db)
        events = repo.query_events(user_id=user_id, workspace_id="career", limit=50)

        job_apps = []
        resume_updates = []

        for e in events:
            if not e.payload:
                continue
            try:
                p = json.loads(e.payload)
            except Exception:
                continue

            if e.event_type == "JOB_APPLIED":
                job_apps.append({"company": p.get("company_name"), "role": p.get("role_title")})
            elif e.event_type == "RESUME_UPDATED":
                resume_updates.append(p.get("summary"))

        return {
            "total_applications_sent": len(job_apps),
            "recent_applications": job_apps[:5],
            "total_resume_updates": len(resume_updates),
            "coaching_insights": self.get_coaching_insights(db, user_id)
        }

    def get_coaching_insights(self, db: Session, user_id: str = "default_user") -> List[str]:
        repo = EventRepository(db)
        events = repo.query_events(user_id=user_id, workspace_id="career", limit=10)
        if not events:
            return ["💼 No career events logged yet. Tell LordSahu: 'Applied to Fischer Jordan'."]
        return [f"💼 Career Momentum: Logged {len(events)} professional milestones."]
