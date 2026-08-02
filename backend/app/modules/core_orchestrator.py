import uuid
import re
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.modules.context_builder import ContextBuilder
from app.modules.prompt_builder import PromptBuilder
from app.modules.llm_provider import LLMProvider
from app.modules.response_validator import ResponseValidator
from app.modules.execution_planner import ExecutionPlanner
from app.modules.execution_engine import ExecutionEngine
from app.modules.workout_state_machine import workout_state_machine
from app.repositories.chat_repository import ChatRepository
from app.repositories.memory_repository import MemoryRepository
from app.schemas import ChatMessageCreate, ChatResponse, MemoryCreate
from app.models import ChatMessageModel

class CoreOrchestrator:
    """
    Pristine Conductor Orchestrator for LordSahu AI Personal OS.
    Includes Fitness Intelligence Module (FIM) Workout Conversation State Machine.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

        self.context_builder = ContextBuilder(db, user_id)
        self.prompt_builder = PromptBuilder()
        self.llm_provider = LLMProvider()
        self.response_validator = ResponseValidator()
        self.planner = ExecutionPlanner()
        self.execution_engine = ExecutionEngine(db, user_id)
        self.chat_repo = ChatRepository(db)
        self.memory_repo = MemoryRepository(db)

    def process_message(self, request: ChatMessageCreate) -> ChatResponse:
        user_text = request.text.strip()
        mode = request.mode.lower() if request.mode else "assistant"
        workspace_id = request.workspace_id or "personal"
        t_lower = user_text.lower()

        # 1. Save User Chat Record
        self.chat_repo.add(ChatMessageModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            sender="user",
            mode=mode,
            text=user_text
        ))

        # Check Active Workout Session State
        w_state = workout_state_machine.get_session_state(self.user_id)
        is_workout_active = w_state.get("state") in ("WORKOUT_STARTED", "COLLECTING_EXERCISES")

        # Conversational State Machine Interceptions
        if "workout completed" in t_lower or "finish workout" in t_lower or "done with workout" in t_lower:
            result = workout_state_machine.finalize_workout(self.user_id, self.db)
            final_reply = result["reply"]
            return self._build_chat_response(mode, final_reply, "LOG_WORKOUT", {}, [])

        if is_workout_active:
            # Parse Exercise pattern: e.g., "Bench Press 20 kg 3 sets 12 reps"
            ex_match = re.search(r"([a-zA-Z\s]+)\s+(\d+(?:\.\d+)?)\s*kg\s+(\d+)\s*sets\s+(\d+)\s*reps", user_text, re.IGNORECASE)
            if ex_match:
                ex_name = ex_match.group(1).strip()
                ex_weight = float(ex_match.group(2))
                ex_sets = int(ex_match.group(3))
                ex_reps = int(ex_match.group(4))

                res = workout_state_machine.add_exercise(self.user_id, ex_name, ex_weight, ex_sets, ex_reps)
                return self._build_chat_response(mode, res["reply"], "LOG_EXERCISE", {}, [])

        if any(k in t_lower for k in ["chest day", "leg day", "arm day", "back day", "shoulder day", "push day", "pull day"]):
            res = workout_state_machine.start_workout(self.user_id, user_text.capitalize(), self.db)
            return self._build_chat_response(mode, res["reply"], "START_WORKOUT", {}, [])

        # Standard Conductor Execution Pipeline
        context = self.context_builder.build_context(active_workspace=workspace_id)
        retrieved_memories = [m["fact"] for m in context.get("memories", [])]

        system_prompt = self.prompt_builder.build_system_prompt(mode, context, retrieved_memories)
        raw_llm_result = self.llm_provider.generate_response(system_prompt, user_text)
        validated = self.response_validator.validate_or_fallback(raw_llm_result, user_text)

        intent = validated["intent"]
        entities = validated["entities"]
        learned_memories = validated["new_memories_learned"]
        reply_text = validated["reply"]

        # Self-Learning Feedback Loop
        for mem in learned_memories:
            fact_str = mem.get("fact") if isinstance(mem, dict) else str(mem)
            m_type = mem.get("memory_type", "PREFERENCE") if isinstance(mem, dict) else "PREFERENCE"
            m_cat = mem.get("category", "general") if isinstance(mem, dict) else "general"

            if fact_str:
                self.memory_repo.add(self.memory_repo.model_cls(
                    user_id=self.user_id,
                    workspace_id=workspace_id,
                    memory_type=m_type,
                    category=m_cat,
                    fact=fact_str,
                    confidence=0.95
                ))
                retrieved_memories.append(fact_str)

        # Multi-Step Execution Plan & Engine Run
        plan = self.planner.plan(validated, user_text)
        execution_outcome = self.execution_engine.execute_plan(plan, workspace_id=workspace_id)

        final_reply = execution_outcome.get("summary")
        if not final_reply or final_reply == "Plan execution completed.":
            final_reply = reply_text or f"Understood Siddhant. Executed in LordSahu OS database."

        generated_events = []
        for res in execution_outcome.get("results", []):
            if res.get("status") == "success" and isinstance(res.get("result"), dict):
                evt_id = res["result"].get("event_id")
                if evt_id:
                    generated_events.append({"id": evt_id, "type": res["tool"].upper()})

        return self._build_chat_response(mode, final_reply, intent, entities, generated_events, retrieved_memories)

    def _build_chat_response(
        self,
        mode: str,
        reply_text: str,
        intent: str,
        entities: Dict[str, Any],
        generated_events: List[Dict[str, Any]],
        memories_retrieved: List[str] = None
    ) -> ChatResponse:
        db_sahu_msg = self.chat_repo.add(ChatMessageModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            sender="lord_sahu",
            mode=mode,
            text=reply_text,
            intent=intent,
            extracted_entities=str(entities),
            generated_events=str(generated_events)
        ))

        return ChatResponse(
            id=db_sahu_msg.id,
            sender="lord_sahu",
            mode=mode,
            text=reply_text,
            intent=intent,
            extracted_entities=[{"key": k, "value": v} for k, v in entities.items()],
            generated_events=generated_events,
            memories_retrieved=memories_retrieved or [],
            tasks_created=[],
            created_at=db_sahu_msg.created_at
        )
