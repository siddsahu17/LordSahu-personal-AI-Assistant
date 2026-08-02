from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class LogExpenseCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        amount = float(params.get("amount") or 0.0)
        category = params.get("category") or "Food & Dining"
        description = params.get("description") or "Expense"

        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="finance",
            source="chat_text",
            event_type="EXPENSE_LOGGED",
            intent="LOG_EXPENSE",
            payload={"amount": amount, "category": category, "description": description}
        ))
        return {
            "status": "success",
            "amount": amount,
            "event_id": evt.id,
            "message": f"Logged expense ₹{amount} for '{description}' [{category}] into Finance Journal."
        }

class LogIncomeCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        amount = float(params.get("amount") or 0.0)
        source = params.get("source") or "Income"
        evt_engine = EventEngine(self.db, self.user_id)
        evt = evt_engine.create_event(EventCreate(
            workspace_id="finance",
            source="chat_text",
            event_type="INCOME_LOGGED",
            intent="LOG_INCOME",
            payload={"amount": amount, "source": source}
        ))
        return {"status": "success", "amount": amount, "event_id": evt.id, "message": f"Logged income ₹{amount} from {source}."}
