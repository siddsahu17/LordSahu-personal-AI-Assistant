import os
import re
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

from app.modules.context_engine import ContextEngine
from app.modules.memory_engine import MemoryEngine
from app.modules.event_engine import EventEngine
from app.modules.goal_engine import GoalEngine
from app.modules.task_engine import TaskEngine
from app.modules.knowledge_engine import KnowledgeEngine
from app.modules.analytics_engine import AnalyticsEngine
from app.modules.report_generator import ReportGenerator
from app.schemas import EventCreate, MemoryCreate, GoalCreate, TaskCreate, ChatMessageCreate, ChatResponse

PERSONA_SYSTEM_INSTRUCTIONS = {
    "assistant": "You are LordSahu, a sharp, efficient, digital Chief of Staff. Speak concisely, clearly, and directly in a clear female voice persona.",
    "coach": "You are LordSahu in Coach Mode. Energetic, high-accountability, direct, and motivating.",
    "focus": "You are LordSahu in Focus Mode. Calm, distraction-free, structured, and deep-work oriented.",
    "reflection": "You are LordSahu in Reflection Mode. Thoughtful, asking deep reflective questions about balance and growth.",
    "planner": "You are LordSahu in Planner Mode. Highly organized, strategic, milestone-focused.",
    "reviewer": "You are LordSahu in Reviewer Mode. Analytical, audit-driven, analyzing metrics and consistency scores."
}

SYSTEM_ORCHESTRATOR_PROMPT = """You are LordSahu, an AI Personal Operating System whose primary interface is conversation.

Persona Instruction:
{persona_instruction}

Self-Learning Feedback Loop Rule:
Analyze the user's message for any new user preferences, corrections, habits, schedule choices, or personal facts (e.g., "I prefer studying in the evening", "Never remind me on Sundays").
If the user provides a preference or habit, output it in "new_memories_learned" list so LordSahu continually adapts and improves over time.

Real User Context Bundle:
- Current Time: {current_time_iso}
- Current Date: {current_date_str}
- Current Weight (kg): {current_weight_kg}
- Active Goals: {active_goals_json}
- Today's Life Events: {todays_events_json}
- Pending Tasks: {pending_tasks_json}
- Learned Memories: {retrieved_memories_json}

User Input Message:
"{user_text}"

Intents Available:
- "QUERY_GOALS": User is asking to list, see, or check their goals.
- "QUERY_EVENTS": User is asking to list, see, or check their logged events/timeline.
- "QUERY_WORKSPACES": User is asking to list or view their workspaces.
- "QUERY_TASKS": User is asking to list or view their tasks/reminders.
- "QUERY_MEMORIES": User is asking to list or see stored memories.
- "CREATE_GOAL", "DELETE_GOAL", "CREATE_TASK", "DELETE_TASK", "DELETE_MEMORY"
- "LOG_WEIGHT", "LOG_STUDY", "LOG_WORKOUT"
- "MORNING_BRIEFING", "GENERAL_CHAT"

Respond ONLY with a JSON object containing keys:
1. "intent": String (One of the intents listed above)
2. "entities": Object (Extracted fields, e.g. {{"goal_title": "DBMS Mastery"}}, {{"task_title": "Finish Assignment"}})
3. "new_memories_learned": Array of objects [{{"memory_type": "PREFERENCE", "category": "general", "fact": "User prefers..."}}]
4. "reply": String (Your detailed persona response answering the user's question directly with clear formatting)
"""

AVAILABLE_WORKSPACES = [
    {"id": "learning", "name": "Learning", "description": "DBMS, SQL, Programming, Courses"},
    {"id": "fitness", "name": "Fitness & Health", "description": "Weight Loss, Workouts, Nutrition"},
    {"id": "career", "name": "Career", "description": "Projects, Internships, Resume, Industry"},
    {"id": "college", "name": "College", "description": "Assignments, Exams, Academics, GPA"},
    {"id": "finance", "name": "Finance", "description": "Budget, Expenses, Savings"},
    {"id": "projects", "name": "Projects", "description": "Software Engineering & AI OS"},
    {"id": "personal", "name": "Personal", "description": "Habits, Journal, Daily Reminders"}
]

class CoreOrchestrator:
    """
    Core Intelligence Orchestrator with Self-Learning AI Memory and Database Query Handlers.
    Answers queries about goals, events, tasks, memories, and workspaces directly from SQLite database.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

        self.context_engine = ContextEngine(db, user_id)
        self.memory_engine = MemoryEngine(db, user_id)
        self.event_engine = EventEngine(db, user_id)
        self.goal_engine = GoalEngine(db, user_id)
        self.task_engine = TaskEngine(db, user_id)
        self.knowledge_engine = KnowledgeEngine(db, user_id)
        self.analytics_engine = AnalyticsEngine(db, user_id)
        self.report_generator = ReportGenerator(db, user_id)

        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
        self.api_base = os.getenv("OPENAI_API_BASE", None)

    def process_message(self, request: ChatMessageCreate) -> ChatResponse:
        user_text = request.text.strip()
        mode = request.mode.lower() if request.mode else "assistant"
        workspace_id = request.workspace_id or "personal"

        # Save User Message Record
        from app.models import ChatMessageModel
        user_chat_rec = ChatMessageModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            sender="user",
            mode=mode,
            text=user_text
        )
        self.db.add(user_chat_rec)
        self.db.commit()

        # Build Context & Retrieve Learned Memories
        context = self.context_engine.build_context()
        retrieved_memories = self.memory_engine.retrieve_relevant_memories(user_text, limit=5)

        # Parse via LangChain or Fallback Parser
        parsed_result = None
        if self.api_key and LANGCHAIN_AVAILABLE:
            parsed_result = self._call_langchain_orchestrator(user_text, mode, context, retrieved_memories)

        if not parsed_result:
            intent, entities, fallback_memories = self._fallback_parse_intent_and_entities(user_text)
            reply_text = self._fallback_generate_response(user_text, mode, intent, entities, context, retrieved_memories)
            parsed_result = {
                "intent": intent,
                "entities": entities,
                "new_memories_learned": fallback_memories,
                "reply": reply_text
            }

        intent = parsed_result.get("intent", "GENERAL_CHAT")
        entities = parsed_result.get("entities", {})
        learned_memories = parsed_result.get("new_memories_learned", [])
        reply_text = parsed_result.get("reply", "")

        # Store Learned Memories
        for mem in learned_memories:
            fact_str = mem.get("fact") if isinstance(mem, dict) else str(mem)
            m_type = mem.get("memory_type", "PREFERENCE") if isinstance(mem, dict) else "PREFERENCE"
            m_cat = mem.get("category", "general") if isinstance(mem, dict) else "general"

            if fact_str:
                self.memory_engine.add_memory(MemoryCreate(
                    memory_type=m_type,
                    category=m_cat,
                    fact=fact_str,
                    confidence=0.95
                ))
                retrieved_memories.append(fact_str)

        generated_events = []
        tasks_created = []

        # --- Handle Query Intents (Goals, Events, Workspaces, Tasks, Memories) ---
        if intent == "QUERY_WORKSPACES":
            reply_text = self._format_workspaces_response()

        elif intent == "QUERY_GOALS":
            reply_text = self._format_goals_response()

        elif intent == "QUERY_EVENTS":
            reply_text = self._format_events_response()

        elif intent == "QUERY_TASKS":
            reply_text = self._format_tasks_response()

        elif intent == "QUERY_MEMORIES":
            reply_text = self._format_memories_response()

        # --- Handle Database Mutation Intents ---
        elif intent == "CREATE_GOAL":
            g_title = entities.get("goal_title") or entities.get("title") or user_text
            g_ws = entities.get("workspace_id") or workspace_id
            g_target = float(entities.get("target_value") or 20.0)
            g_metric = entities.get("target_metric") or "hours"
            g_priority = entities.get("priority") or "HIGH"

            g_obj = self.goal_engine.create_goal(GoalCreate(
                title=g_title,
                workspace_id=g_ws,
                description=f"Goal created via LordSahu Chat",
                target_value=g_target,
                target_metric=g_metric,
                priority=g_priority
            ))
            evt = self.event_engine.create_event(EventCreate(
                workspace_id=g_ws,
                source="chat_text",
                event_type="GOAL_CREATED",
                intent=intent,
                entities=[{"type": "goal_title", "value": g_title}],
                payload={"goal_id": g_obj.id, "title": g_title},
                confidence=0.98
            ))
            generated_events.append({"id": evt.id, "type": "GOAL_CREATED", "title": g_title})
            reply_text = f"Added living goal '{g_title}' to your database under '{g_ws}' workspace."

        elif intent == "DELETE_GOAL":
            g_title = entities.get("goal_title") or entities.get("title") or user_text
            deleted_title = self.goal_engine.delete_goal(g_title)
            if deleted_title:
                evt = self.event_engine.create_event(EventCreate(
                    workspace_id=workspace_id,
                    source="chat_text",
                    event_type="GOAL_DELETED",
                    intent=intent,
                    entities=[{"type": "goal_title", "value": deleted_title}],
                    payload={"title": deleted_title},
                    confidence=0.98
                ))
                generated_events.append({"id": evt.id, "type": "GOAL_DELETED", "title": deleted_title})
                reply_text = f"Deleted goal '{deleted_title}' from database."
            else:
                reply_text = f"Could not find a goal matching '{g_title}' to delete."

        elif intent == "CREATE_TASK":
            task_title = entities.get("task_title") or user_text
            t_obj = self.task_engine.create_task(TaskCreate(
                workspace_id=workspace_id,
                title=task_title,
                priority="HIGH",
                due_date=datetime.now(timezone.utc) + timedelta(days=1)
            ))
            tasks_created.append({"id": t_obj.id, "title": t_obj.title})
            evt = self.event_engine.create_event(EventCreate(
                workspace_id=workspace_id,
                source="chat_text",
                event_type="TASK_CREATED",
                intent=intent,
                entities=[{"type": "task_title", "value": task_title}],
                payload={"task_id": t_obj.id, "title": task_title},
                confidence=0.95
            ))
            generated_events.append({"id": evt.id, "type": "TASK_CREATED", "title": task_title})
            reply_text = f"Scheduled task '{task_title}'."

        elif intent == "DELETE_TASK":
            t_title = entities.get("task_title") or user_text
            deleted_title = self.task_engine.delete_task(t_title)
            if deleted_title:
                reply_text = f"Deleted task '{deleted_title}' from database."
            else:
                reply_text = f"Could not find task matching '{t_title}' to delete."

        elif intent == "DELETE_MEMORY":
            m_fact = entities.get("memory_fact") or user_text
            deleted_fact = self.memory_engine.delete_memory(m_fact)
            if deleted_fact:
                reply_text = f"Deleted memory '{deleted_fact}' from database."
            else:
                reply_text = f"Could not find memory matching '{m_fact}' to delete."

        elif intent == "LOG_WEIGHT":
            weight_val = entities.get("weight_kg")
            if weight_val:
                evt = self.event_engine.create_event(EventCreate(
                    workspace_id="fitness",
                    source="chat_text",
                    event_type="WEIGHT_LOGGED",
                    intent=intent,
                    entities=[{"type": "weight_kg", "value": weight_val}],
                    payload={"weight_kg": weight_val, "raw_input": user_text},
                    confidence=0.98
                ))
                generated_events.append({"id": evt.id, "type": "WEIGHT_LOGGED", "weight_kg": weight_val})
                self.memory_engine.add_memory(MemoryCreate(
                    memory_type="FACT",
                    category="fitness",
                    fact=f"Current body weight recorded as {weight_val} kg",
                    confidence=0.98,
                    source_event_id=evt.id
                ))
                reply_text = f"Recorded {weight_val} kg into database Event Store."

        elif intent == "LOG_STUDY":
            subject = entities.get("subject") or "General Study"
            duration = entities.get("duration_hours") or 1.0
            evt = self.event_engine.create_event(EventCreate(
                workspace_id="learning",
                source="chat_text",
                event_type="STUDY_SESSION",
                intent=intent,
                entities=[
                    {"type": "subject", "value": subject},
                    {"type": "duration_hours", "value": duration}
                ],
                payload={"subject": subject, "duration_hours": duration, "notes": user_text},
                confidence=0.95
            ))
            generated_events.append({"id": evt.id, "type": "STUDY_SESSION", "subject": subject, "duration_hours": duration})
            reply_text = f"Recorded {duration} hours of '{subject}' into database Event Store."

        elif intent == "LOG_WORKOUT":
            workout_type = entities.get("workout_type") or "Workout"
            duration = entities.get("duration_hours") or 0.5
            evt = self.event_engine.create_event(EventCreate(
                workspace_id="fitness",
                source="chat_text",
                event_type="WORKOUT_COMPLETED",
                intent=intent,
                entities=[
                    {"type": "workout_type", "value": workout_type},
                    {"type": "duration_hours", "value": duration}
                ],
                payload={"workout_type": workout_type, "duration_hours": duration},
                confidence=0.90
            ))
            generated_events.append({"id": evt.id, "type": "WORKOUT_COMPLETED", "workout_type": workout_type})
            reply_text = f"Recorded '{workout_type}' session into database Event Store."

        elif not reply_text:
            reply_text = f"I've registered your update in LordSahu Operating System context."

        # Save AI Response Record
        db_sahu_msg = ChatMessageModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            sender="lord_sahu",
            mode=mode,
            text=reply_text,
            intent=intent,
            extracted_entities=json.dumps(entities),
            generated_events=json.dumps(generated_events)
        )
        self.db.add(db_sahu_msg)
        self.db.commit()

        return ChatResponse(
            id=db_sahu_msg.id,
            sender="lord_sahu",
            mode=mode,
            text=reply_text,
            intent=intent,
            extracted_entities=[{"key": k, "value": v} for k, v in entities.items()],
            generated_events=generated_events,
            memories_retrieved=retrieved_memories,
            tasks_created=tasks_created,
            created_at=db_sahu_msg.created_at
        )

    def _format_workspaces_response(self) -> str:
        lines = ["Here are your active workspaces in LordSahu AI Personal OS:"]
        for i, w in enumerate(AVAILABLE_WORKSPACES, 1):
            lines.append(f"{i}. **{w['name']}** (`{w['id']}`): {w['description']}")
        return "\n".join(lines)

    def _format_goals_response(self) -> str:
        goals = self.goal_engine.list_goals()
        if not goals:
            return "You currently have no active goals in your database. You can add one anytime by chatting e.g. 'Add goal to learn Rust in 30 hours'!"
        lines = [f"Here are your active living goals in your database ({len(goals)} total):"]
        for g in goals:
            lines.append(
                f"• **{g['title']}** [{g['workspace_id'].upper()}]\n"
                f"  - Progress: {g['inferred_progress']}%\n"
                f"  - Priority: {g['priority']} | Status: {g['status']}"
            )
        return "\n\n".join(lines)

    def _format_events_response(self) -> str:
        events = self.event_engine.query_events(limit=10)
        if not events:
            return "No life events logged in your Event Store yet. Start logging weight, study sessions, or workouts via chat!"
        lines = [f"Here are your recent life events recorded in your Event Store ({len(events)} recent):"]
        for e in events:
            date_str = e['created_at'][:16].replace('T', ' ') if e.get('created_at') else ''
            lines.append(f"• **{e['event_type']}** [{e['workspace_id'].upper()}] - {date_str}")
        return "\n".join(lines)

    def _format_tasks_response(self) -> str:
        tasks = self.task_engine.list_tasks()
        if not tasks:
            return "You have no pending tasks in your database. You can schedule one by saying e.g. 'Remind me tomorrow to submit DBMS assignment'!"
        lines = [f"Here are your tasks in your database ({len(tasks)} total):"]
        for t in tasks:
            lines.append(f"• **{t['title']}** (Status: {t['status']}, Priority: {t['priority']})")
        return "\n".join(lines)

    def _format_memories_response(self) -> str:
        memories = self.memory_engine.list_memories()
        if not memories:
            return "No memory facts stored in your database yet."
        lines = [f"Here are your stored memory facts in your database ({len(memories)} total):"]
        for m in memories:
            lines.append(f"• [{m.memory_type}] {m.fact}")
        return "\n".join(lines)

    def _call_langchain_orchestrator(self, user_text: str, mode: str, context: Dict[str, Any], memories: List[str]) -> Optional[Dict[str, Any]]:
        try:
            kwargs = {
                "openai_api_key": self.api_key,
                "model_name": self.model_name,
                "temperature": 0.2
            }
            if self.api_base:
                kwargs["openai_api_base"] = self.api_base

            llm = ChatOpenAI(**kwargs)
            prompt = ChatPromptTemplate.from_template(SYSTEM_ORCHESTRATOR_PROMPT)
            parser = JsonOutputParser()

            chain = prompt | llm | parser
            persona_inst = PERSONA_SYSTEM_INSTRUCTIONS.get(mode, PERSONA_SYSTEM_INSTRUCTIONS["assistant"])

            res = chain.invoke({
                "persona_instruction": persona_inst,
                "current_time_iso": context.get("current_time_iso", ""),
                "current_date_str": context.get("current_date_str", ""),
                "current_weight_kg": context.get("current_weight_kg", "not set"),
                "active_goals_json": json.dumps(context.get("active_goals", [])),
                "todays_events_json": json.dumps(context.get("todays_events", [])),
                "pending_tasks_json": json.dumps(context.get("pending_tasks", [])),
                "retrieved_memories_json": json.dumps(memories),
                "user_text": user_text
            })
            return res
        except Exception as e:
            print(f"[LangChain Orchestrator Warning]: {e}. Using fallback parser.")
            return None

    def _fallback_parse_intent_and_entities(self, text: str) -> tuple[str, Dict[str, Any], List[Dict[str, Any]]]:
        t_lower = text.lower()
        entities = {}
        learned_memories = []

        # Detect Query Intents
        if any(q in t_lower for q in ["workspace", "workspaces", "all the works"]):
            return "QUERY_WORKSPACES", entities, learned_memories

        if any(q in t_lower for q in ["all my goals", "all goals", "list goals", "my goals", "what are my goals", "goals and events"]):
            if "event" in t_lower and "goal" in t_lower:
                return "QUERY_GOALS", entities, learned_memories
            return "QUERY_GOALS", entities, learned_memories

        if any(q in t_lower for q in ["all events", "list events", "my events", "events stream", "timeline events"]):
            return "QUERY_EVENTS", entities, learned_memories

        if any(q in t_lower for q in ["all tasks", "list tasks", "my tasks", "pending tasks", "todos"]):
            return "QUERY_TASKS", entities, learned_memories

        if any(q in t_lower for q in ["all memories", "list memories", "my memories", "memory facts"]):
            return "QUERY_MEMORIES", entities, learned_memories

        # Detect Preferences
        pref_triggers = ["i prefer", "i like", "i hate", "don't remind", "always", "never", "remember that"]
        for tr in pref_triggers:
            if tr in t_lower:
                learned_memories.append({
                    "memory_type": "PREFERENCE" if "prefer" in tr or "like" in tr else "HABIT",
                    "category": "general",
                    "fact": text
                })
                break

        # Detect Goal mutations
        if "delete goal" in t_lower or "remove goal" in t_lower:
            intent = "DELETE_GOAL"
            clean_title = re.sub(r"(delete|remove)\s+goal\s*", "", t_lower).strip()
            entities["goal_title"] = clean_title or text
            return intent, entities, learned_memories

        if "add goal" in t_lower or "create goal" in t_lower or "new goal" in t_lower:
            intent = "CREATE_GOAL"
            clean_title = re.sub(r"(add|create|new)\s+goal\s*", "", t_lower).strip()
            entities["goal_title"] = clean_title or text
            return intent, entities, learned_memories

        if "delete task" in t_lower or "remove task" in t_lower:
            intent = "DELETE_TASK"
            clean_title = re.sub(r"(delete|remove)\s+task\s*", "", t_lower).strip()
            entities["task_title"] = clean_title or text
            return intent, entities, learned_memories

        if "delete memory" in t_lower or "forget memory" in t_lower:
            intent = "DELETE_MEMORY"
            clean_fact = re.sub(r"(delete|forget)\s+(memory|that)?\s*", "", t_lower).strip()
            entities["memory_fact"] = clean_fact or text
            return intent, entities, learned_memories

        weight_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:kg|kilos|pounds|lbs)", t_lower)
        if "weight" in t_lower or weight_match or "weigh" in t_lower:
            intent = "LOG_WEIGHT"
            if weight_match:
                entities["weight_kg"] = float(weight_match.group(1))
            return intent, entities, learned_memories

        study_keywords = ["study", "studied", "learning", "revised", "read", "sql", "dbms", "lecture", "assignment"]
        if any(k in t_lower for k in study_keywords):
            intent = "LOG_STUDY"
            dur_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:hours|hrs|hr|hour|mins|minutes)", t_lower)
            if dur_match:
                val = float(dur_match.group(1))
                if "min" in dur_match.group(0):
                    entities["duration_hours"] = round(val / 60.0, 2)
                else:
                    entities["duration_hours"] = val
            else:
                entities["duration_hours"] = 1.0

            if "sql" in t_lower:
                entities["subject"] = "SQL Joins & Queries"
            elif "dbms" in t_lower:
                entities["subject"] = "DBMS"
            else:
                entities["subject"] = "General Learning"
            return intent, entities, learned_memories

        workout_keywords = ["workout", "gym", "cardio", "ran", "running", "exercise", "steps", "pushups"]
        if any(k in t_lower for k in workout_keywords):
            intent = "LOG_WORKOUT"
            entities["workout_type"] = "Cardio & Fitness"
            entities["duration_hours"] = 0.5
            return intent, entities, learned_memories

        task_keywords = ["remind", "reminder", "task", "todo", "schedule"]
        if any(k in t_lower for k in task_keywords):
            intent = "CREATE_TASK"
            entities["task_title"] = text
            return intent, entities, learned_memories

        if "morning" in t_lower or "briefing" in t_lower or "hello" in t_lower or "hi" in t_lower:
            intent = "MORNING_BRIEFING"
            return intent, entities, learned_memories

        intent = "LEARN_PREFERENCE" if learned_memories else "GENERAL_CHAT"
        return intent, entities, learned_memories

    def _fallback_generate_response(
        self,
        user_text: str,
        mode: str,
        intent: str,
        entities: Dict[str, Any],
        context: Dict[str, Any],
        memories: List[str]
    ) -> str:
        weight_str = f"{context['current_weight_kg']} kg" if context['current_weight_kg'] else "not recorded yet"

        if intent == "MORNING_BRIEFING":
            return (
                f"Good morning Siddhant. Current Weight: {weight_str}. "
                f"Active Goals: {len(context['active_goals'])}. Todays Events: {len(context['todays_events'])}. "
                f"How can LordSahu assist your life timeline today?"
            )

        if intent == "LEARN_PREFERENCE":
            return f"Learned Preference: Added '{user_text}' to LordSahu permanent memory bank."

        if intent == "QUERY_WORKSPACES":
            return self._format_workspaces_response()

        if intent == "QUERY_GOALS":
            return self._format_goals_response()

        if intent == "QUERY_EVENTS":
            return self._format_events_response()

        if intent == "QUERY_TASKS":
            return self._format_tasks_response()

        if intent == "QUERY_MEMORIES":
            return self._format_memories_response()

        # Dynamic fallback response referencing real context
        active_goals_cnt = len(context.get("active_goals", []))
        todays_events_cnt = len(context.get("todays_events", []))
        return f"Understood Siddhant. Currently managing {active_goals_cnt} active goals and {todays_events_cnt} events recorded today in your LordSahu database."
