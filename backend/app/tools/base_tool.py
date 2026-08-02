from typing import Dict, Any, Optional

class BaseTool:
    """
    Base Tool interface in LordSahu AI OS.
    Tools are deterministic, independent plugins executed by the Execution Engine.
    The LLM NEVER mutates the database directly; it selects Tools.
    """
    name: str = "base_tool"
    description: str = "Base tool description"
    version: str = "1.0.0"
    category: str = "general"
    requires_permission: bool = False
    timeout_seconds: int = 10

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "requires_permission": self.requires_permission,
            "timeout_seconds": self.timeout_seconds
        }

    def execute(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        raise NotImplementedError
