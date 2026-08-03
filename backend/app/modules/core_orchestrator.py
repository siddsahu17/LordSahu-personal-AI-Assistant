import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.modules.life_entry_engine import LifeEntryEngine
from app.modules.daily_planner_engine import DailyPlannerEngine
from app.repositories.chat_repository import ChatRepository
from app.schemas import ChatMessageCreate, ChatResponse
from app.models import ChatMessageModel

class CoreOrchestrator:
    """
    Conductor Orchestrator for LordSahu V1.4 (The 3 Canonical Objects Lifecycle).
    Routes conversational inputs across LifeEntry Engine & Daily Planner Engine.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self.life_engine = LifeEntryEngine(db, user_id)
        self.planner_engine = DailyPlannerEngine(db, user_id)
        self.chat_repo = ChatRepository(db)

    def process_message(self, request: ChatMessageCreate) -> ChatResponse:
        user_text = request.text.strip()
        mode = request.mode.lower() if request.mode else "assistant"
        t_lower = user_text.lower()

        # 1. Save User Chat Record
        self.chat_repo.add(ChatMessageModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            sender="user",
            mode=mode,
            text=user_text
        ))

        # Conversational Planner Commands Interception
        if "carry forward" in t_lower:
            res = self.planner_engine.carry_forward_unfinished()
            reply = res["message"]
            intent = "CARRY_FORWARD_PLANNER"
        elif "morning brief" in t_lower or "generate planner" in t_lower or "today's brief" in t_lower:
            res = self.planner_engine.generate_morning_brief()
            reply = f"{res['morning_brief']} Planner agenda generated with {res['planner']['total_items']} items."
            intent = "MORNING_BRIEF_PLANNER"
        elif "evening shutdown" in t_lower or "evening review" in t_lower:
            res = self.planner_engine.run_evening_shutdown()
            reply = f"{res['review_prompt']} ({res['completed_count']} items completed today, {res['remaining_count']} remaining)."
            intent = "EVENING_SHUTDOWN_PLANNER"
        elif "add planner" in t_lower or "plan to" in t_lower:
            clean_title = user_text.replace("add planner", "").replace("plan to", "").strip() or user_text
            res = self.planner_engine.add_item_to_today(clean_title)
            reply = res["message"]
            intent = "ADD_PLANNER_ITEM"
        elif "actually" in t_lower or "change" in t_lower or "correct" in t_lower or "update entry" in t_lower:
            res = self.life_engine.update_matching_entry(user_text, user_text)
            reply = res["message"]
            intent = "UPDATE_LIFE_ENTRY"
        elif "delete entry" in t_lower or "remove entry" in t_lower:
            res = self.life_engine.soft_delete_matching_entry(user_text)
            reply = res["message"]
            intent = "DELETE_LIFE_ENTRY"
        else:
            # Default Conversational LifeEntry Logging
            res = self.life_engine.process_natural_input(user_text)
            doms_str = ", ".join([d.capitalize() for d in res["domains"]])
            reply = f"Recorded into **{doms_str}** journal. {res['message']}"
            intent = "ADD_LIFE_ENTRY"

        # 2. Save AI Response Record
        db_sahu_msg = self.chat_repo.add(ChatMessageModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            sender="lord_sahu",
            mode=mode,
            text=reply,
            intent=intent,
            extracted_entities=str(res)
        ))

        return ChatResponse(
            id=db_sahu_msg.id,
            sender="lord_sahu",
            mode=mode,
            text=reply,
            intent=intent,
            extracted_entities=[{"key": k, "value": str(v)} for k, v in res.items() if k != "message"],
            generated_events=[],
            memories_retrieved=[],
            tasks_created=[],
            created_at=db_sahu_msg.created_at
        )
