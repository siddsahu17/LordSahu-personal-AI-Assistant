from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.tools.base_tool import BaseTool

class BaseWorkspaceModule:
    """
    Abstract Workspace SDK Base Module in LordSahu AI OS.
    Standardized interface implemented by all 7 Workspace Intelligence Modules.
    """
    workspace_id: str = "personal"
    workspace_name: str = "Personal"

    def get_skill_tools(self) -> List[BaseTool]:
        raise NotImplementedError

    def get_analytics_overview(self, db: Session, user_id: str = "default_user") -> Dict[str, Any]:
        raise NotImplementedError

    def get_coaching_insights(self, db: Session, user_id: str = "default_user") -> List[str]:
        raise NotImplementedError
