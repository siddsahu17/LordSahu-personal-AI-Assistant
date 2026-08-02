from typing import Dict, Any, List, Optional
from app.tools.base_tool import BaseTool

class ToolRegistry:
    """
    ToolRegistry singleton holding all registered tools across all 7 domain skills in LordSahu AI OS.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools: Dict[str, BaseTool] = {}
            cls._instance._register_default_skills()
        return cls._instance

    def register(self, tool: BaseTool) -> None:
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self.tools.get(name)

    def list_tools_metadata(self) -> List[Dict[str, Any]]:
        return [tool.get_metadata() for tool in self.tools.values()]

    def _register_default_skills(self):
        from app.skills.goal_skill import GoalSkill
        from app.skills.fitness_skill import FitnessSkill
        from app.skills.calendar_skill import CalendarSkill
        from app.skills.learning_skill import LearningSkill
        from app.skills.memory_skill import MemorySkill
        from app.skills.career_skill import CareerSkill
        from app.skills.college_skill import CollegeSkill
        from app.skills.finance_skill import FinanceSkill
        from app.skills.personal_skill import PersonalSkill
        from app.skills.project_skill import ProjectSkill

        skills = [
            GoalSkill(), FitnessSkill(), CalendarSkill(), LearningSkill(), MemorySkill(),
            CareerSkill(), CollegeSkill(), FinanceSkill(), PersonalSkill(), ProjectSkill()
        ]
        for s in skills:
            for t in s.get_tools():
                self.register(t)

# Global Singleton
tool_registry = ToolRegistry()
