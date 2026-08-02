from typing import Dict, Any
from sqlalchemy.orm import Session
from app.commands.base_command import BaseCommand
from app.repositories.memory_repository import MemoryRepository

class CreateMemoryCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        fact = params.get("fact") or "Fact memory"
        memory_type = params.get("memory_type") or "PREFERENCE"
        category = params.get("category") or "general"
        workspace_id = params.get("workspace_id") or "personal"

        repo = MemoryRepository(self.db)
        mem = repo.add(repo.model_cls(
            user_id=self.user_id,
            workspace_id=workspace_id,
            memory_type=memory_type,
            category=category,
            fact=fact,
            confidence=0.95
        ))
        return {
            "status": "success",
            "memory_id": mem.id,
            "fact": mem.fact,
            "message": f"Stored memory fact: '{fact}'."
        }

class DeleteMemoryCommand(BaseCommand):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        fact = params.get("fact")
        repo = MemoryRepository(self.db)
        mem = repo.find_by_fact_or_id(self.user_id, fact)
        if mem:
            deleted_fact = mem.fact
            repo.delete(mem)
            return {"status": "success", "message": f"Deleted memory: '{deleted_fact}'."}
        return {"status": "error", "message": f"Memory matching '{fact}' not found."}
