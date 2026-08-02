from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.skills.base_skill import BaseSkill
from app.tools.base_tool import BaseTool
from app.commands.finance_commands import LogExpenseCommand, LogIncomeCommand

class LogExpenseTool(BaseTool):
    name = "log_expense"
    description = "Log financial expense into Finance Journal."
    category = "finance"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogExpenseCommand(db, user_id)
        return cmd.execute(params)

class LogIncomeTool(BaseTool):
    name = "log_income"
    description = "Log income or earnings into Finance Journal."
    category = "finance"

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        db: Session = context["db"]
        user_id = context.get("user_id", "default_user")
        cmd = LogIncomeCommand(db, user_id)
        return cmd.execute(params)

class FinanceSkill(BaseSkill):
    name = "finance_skill"
    description = "Finance Intelligence Module tools (expenses, income, subscriptions, savings)."

    def get_tools(self) -> List[BaseTool]:
        return [LogExpenseTool(), LogIncomeTool()]
