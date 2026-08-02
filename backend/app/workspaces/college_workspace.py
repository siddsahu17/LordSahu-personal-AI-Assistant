import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.workspaces.base_workspace import BaseWorkspaceModule
from app.tools.base_tool import BaseTool
from app.skills.college_skill import CollegeSkill
from app.repositories.event_repository import EventRepository

class CollegeWorkspace(BaseWorkspaceModule):
    workspace_id = "college"
    workspace_name = "College Intelligence Module"

    def get_skill_tools(self) -> List[BaseTool]:
        return CollegeSkill().get_tools()

    def get_analytics_overview(self, db: Session, user_id: str = "default_user") -> Dict[str, Any]:
        repo = EventRepository(db)
        events = repo.query_events(user_id=user_id, workspace_id="college", limit=50)

        attended = 0
        missed = 0
        assignments = []

        for e in events:
            if not e.payload:
                continue
            try:
                p = json.loads(e.payload)
            except Exception:
                continue

            if e.event_type == "LECTURE_ATTENDED":
                attended += 1
            elif e.event_type == "LECTURE_MISSED":
                missed += 1
            elif e.event_type == "ASSIGNMENT_COMPLETED":
                assignments.append(p.get("title"))

        total_lectures = attended + missed
        attendance_pct = round((attended / total_lectures) * 100, 1) if total_lectures > 0 else 100.0

        return {
            "attendance_percentage": attendance_pct,
            "lectures_attended": attended,
            "lectures_missed": missed,
            "completed_assignments": assignments[:5],
            "coaching_insights": self.get_coaching_insights(db, user_id)
        }

    def get_coaching_insights(self, db: Session, user_id: str = "default_user") -> List[str]:
        return ["🎓 Keep up the academic momentum! Log lectures & assignment progress anytime."]
