import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.modules.context_builder import ContextBuilder
from app.modules.prompt_builder import PromptBuilder
from app.modules.llm_provider import LLMProvider
from app.modules.response_validator import ResponseValidator
from app.modules.capability_registry import CapabilityRegistry
from app.repositories.chat_repository import ChatRepository
from app.repositories.memory_repository import MemoryRepository
from app.schemas import ChatMessageCreate, ChatResponse, MemoryCreate
from app.models import ChatMessageModel

class CoreOrchestrator:
    """
    Pristine Conductor Orchestrator for LordSahu AI Personal OS.
    Executes a decoupled Clean Architecture pipeline:
    ContextBuilder -> PromptBuilder -> LLMProvider -> ResponseValidator -> CapabilityRegistry -> EventBus
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

        self.context_builder = ContextBuilder(db, user_id)
        self.prompt_builder = PromptBuilder()
        self.llm_provider = LLMProvider()
        self.response_validator = ResponseValidator()
        self.capability_registry = CapabilityRegistry(db)
        self.chat_repo = ChatRepository(db)
        self.memory_repo = MemoryRepository(db)

    def process_message(self, request: ChatMessageCreate) -> ChatResponse:
        user_text = request.text.strip()
        mode = request.mode.lower() if request.mode else "assistant"
        workspace_id = request.workspace_id or "personal"

        # 1. Save User Chat Record into DB via ChatRepository
        self.chat_repo.add(ChatMessageModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            sender="user",
            mode=mode,
            text=user_text
        ))

        # 2. Context Builder Gathers Full Context Object
        context = self.context_builder.build_context(active_workspace=workspace_id)
        retrieved_memories = [m["fact"] for m in context.get("memories", [])]

        # 3. Prompt Builder Creates Persona System Prompt
        system_prompt = self.prompt_builder.build_system_prompt(mode, context, retrieved_memories)

        # 4. LLM Provider Generates Response (Direct OpenAI SDK)
        raw_llm_result = self.llm_provider.generate_response(system_prompt, user_text)

        # 5. Response Validator Enforces Schema Integrity & Fallbacks
        validated = self.response_validator.validate_or_fallback(raw_llm_result, user_text)

        intent = validated["intent"]
        entities = validated["entities"]
        learned_memories = validated["new_memories_learned"]
        reply_text = validated["reply"]

        # 6. Memory Decay & Self-Learning Feedback Loop
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

        # 7. Capability Registry Resolves & Dispatches Intent Capability
        cap_result = self.capability_registry.dispatch(intent, self.user_id, workspace_id, entities, user_text)

        # Use capability reply if available, otherwise LLM validated reply
        final_reply = cap_result["reply"] if cap_result.get("reply") else reply_text
        if not final_reply:
            active_goals_cnt = len(context.get("active_goals", []))
            final_reply = f"Registered in LordSahu OS context. Managing {active_goals_cnt} active goals."

        generated_events = cap_result.get("events", [])
        tasks_created = cap_result.get("tasks", [])

        # 8. Save AI Response Record via ChatRepository
        db_sahu_msg = self.chat_repo.add(ChatMessageModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            sender="lord_sahu",
            mode=mode,
            text=final_reply,
            intent=intent,
            extracted_entities=str(entities),
            generated_events=str(generated_events)
        ))

        return ChatResponse(
            id=db_sahu_msg.id,
            sender="lord_sahu",
            mode=mode,
            text=final_reply,
            intent=intent,
            extracted_entities=[{"key": k, "value": v} for k, v in entities.items()],
            generated_events=generated_events,
            memories_retrieved=retrieved_memories,
            tasks_created=tasks_created,
            created_at=db_sahu_msg.created_at
        )
