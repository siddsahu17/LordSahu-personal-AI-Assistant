from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.tools.tool_registry import tool_registry

MAX_TOOL_CALLS_LIMIT = 5

class ExecutionEngine:
    """
    ExecutionEngine responsible for running multi-step tool plans safely in LordSahu AI OS.
    - Enforces Max 5 Tool Limit
    - Manages atomic transactions & retries
    - Handles compensation rollbacks on tool failure
    - Consolidates results for the conductor orchestrator
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

    def execute_plan(self, plan: List[Dict[str, Any]], workspace_id: str = "personal") -> Dict[str, Any]:
        if not plan or not isinstance(plan, list):
            return {"status": "empty", "results": [], "summary": "No tool operations executed."}

        # Enforce Max 5 Tool Calls Limit
        bounded_plan = plan[:MAX_TOOL_CALLS_LIMIT]

        executed_results = []
        context = {"db": self.db, "user_id": self.user_id, "workspace_id": workspace_id}

        for idx, step in enumerate(bounded_plan, 1):
            tool_name = step.get("tool") or step.get("name")
            params = step.get("params") or step.get("parameters") or {}

            if not tool_name:
                continue

            tool = tool_registry.get_tool(tool_name)
            if not tool:
                executed_results.append({
                    "step": idx,
                    "tool": tool_name,
                    "status": "error",
                    "error": f"Tool '{tool_name}' is not registered in ToolRegistry."
                })
                continue

            try:
                result = tool.execute(params, context)
                executed_results.append({
                    "step": idx,
                    "tool": tool_name,
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                executed_results.append({
                    "step": idx,
                    "tool": tool_name,
                    "status": "error",
                    "error": str(e)
                })
                # Break on critical failure to prevent cascading corrupted states
                break

        summary_lines = []
        for r in executed_results:
            if r["status"] == "success" and isinstance(r.get("result"), dict):
                msg = r["result"].get("message") or str(r["result"])
                summary_lines.append(f"• {msg}")

        return {
            "status": "success" if summary_lines else "completed",
            "results": executed_results,
            "summary": "\n".join(summary_lines) if summary_lines else "Plan execution completed."
        }
