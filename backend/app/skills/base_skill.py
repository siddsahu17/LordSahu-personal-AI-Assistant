from typing import List, Dict, Any
from app.tools.base_tool import BaseTool

class BaseSkill:
    """
    Base Skill grouping related tools into domain capabilities.
    """
    name: str = "base_skill"
    description: str = "Base skill grouping"

    def get_tools(self) -> List[BaseTool]:
        raise NotImplementedError
