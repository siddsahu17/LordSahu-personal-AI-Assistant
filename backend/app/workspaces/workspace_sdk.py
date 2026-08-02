from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.workspaces.base_workspace import BaseWorkspaceModule

class WorkspaceSDKRegistry:
    """
    WorkspaceSDKRegistry holding all 7 domain workspace modules in LordSahu AI OS.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorkspaceSDKRegistry, cls).__new__(cls)
            cls._instance.workspaces: Dict[str, BaseWorkspaceModule] = {}
            cls._instance._register_default_workspaces()
        return cls._instance

    def register(self, module: BaseWorkspaceModule) -> None:
        self.workspaces[module.workspace_id] = module

    def get_workspace(self, workspace_id: str) -> Optional[BaseWorkspaceModule]:
        return self.workspaces.get(workspace_id)

    def list_workspaces(self) -> List[Dict[str, str]]:
        return [
            {"id": w.workspace_id, "name": w.workspace_name}
            for w in self.workspaces.values()
        ]

    def _register_default_workspaces(self):
        from app.workspaces.learning_workspace import LearningWorkspace
        from app.workspaces.career_workspace import CareerWorkspace
        from app.workspaces.college_workspace import CollegeWorkspace
        from app.workspaces.finance_workspace import FinanceWorkspace
        from app.workspaces.personal_workspace import PersonalWorkspace
        from app.workspaces.projects_workspace import ProjectsWorkspace
        from app.workspaces.fitness_workspace import FitnessWorkspace

        modules = [
            LearningWorkspace(), CareerWorkspace(), CollegeWorkspace(),
            FinanceWorkspace(), PersonalWorkspace(), ProjectsWorkspace(), FitnessWorkspace()
        ]
        for m in modules:
            self.register(m)

# Global Workspace SDK Singleton
workspace_sdk = WorkspaceSDKRegistry()
