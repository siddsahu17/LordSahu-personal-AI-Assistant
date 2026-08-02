import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.workspaces.base_workspace import BaseWorkspaceModule
from app.tools.base_tool import BaseTool
from app.skills.finance_skill import FinanceSkill
from app.repositories.event_repository import EventRepository

class FinanceWorkspace(BaseWorkspaceModule):
    workspace_id = "finance"
    workspace_name = "Finance Intelligence Module"

    def get_skill_tools(self) -> List[BaseTool]:
        return FinanceSkill().get_tools()

    def get_analytics_overview(self, db: Session, user_id: str = "default_user") -> Dict[str, Any]:
        repo = EventRepository(db)
        events = repo.query_events(user_id=user_id, workspace_id="finance", limit=50)

        total_expenses = 0.0
        total_income = 0.0
        recent_expenses = []

        for e in events:
            if not e.payload:
                continue
            try:
                p = json.loads(e.payload)
            except Exception:
                continue

            if e.event_type == "EXPENSE_LOGGED":
                amt = float(p.get("amount") or 0.0)
                total_expenses += amt
                recent_expenses.append({"amount": amt, "description": p.get("description"), "category": p.get("category")})
            elif e.event_type == "INCOME_LOGGED":
                total_income += float(p.get("amount") or 0.0)

        return {
            "total_expenses_recorded": round(total_expenses, 2),
            "total_income_recorded": round(total_income, 2),
            "net_balance": round(total_income - total_expenses, 2),
            "recent_expenses": recent_expenses[:5],
            "coaching_insights": self.get_coaching_insights(db, user_id)
        }

    def get_coaching_insights(self, db: Session, user_id: str = "default_user") -> List[str]:
        return ["💰 Financial Journal Active. Say 'Spent ₹250 on lunch' to log expenses."]
