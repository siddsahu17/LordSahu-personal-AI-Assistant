import re
from typing import Dict, Any, List, Tuple

VALID_INTENTS = {
    "QUERY_WORKSPACES", "QUERY_GOALS", "QUERY_EVENTS", "QUERY_TASKS", "QUERY_MEMORIES",
    "CREATE_GOAL", "DELETE_GOAL", "CREATE_TASK", "DELETE_TASK", "DELETE_MEMORY",
    "LOG_WEIGHT", "LOG_STUDY", "LOG_WORKOUT", "MORNING_BRIEFING", "LEARN_PREFERENCE", "GENERAL_CHAT"
}

class ResponseValidator:
    """
    AI Response Validator ensuring LLM JSON outputs adhere strictly to schema specs.
    Includes deterministic pattern-matching fallback when LLM is unavailable or un-parseable.
    """
    def validate_or_fallback(self, raw_llm_result: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        if raw_llm_result and isinstance(raw_llm_result, dict):
            intent = raw_llm_result.get("intent", "GENERAL_CHAT")
            if intent in VALID_INTENTS:
                entities = raw_llm_result.get("entities", {})
                new_memories = raw_llm_result.get("new_memories_learned", [])
                reply = raw_llm_result.get("reply", "")

                return {
                    "intent": intent,
                    "entities": entities if isinstance(entities, dict) else {},
                    "new_memories_learned": new_memories if isinstance(new_memories, list) else [],
                    "reply": reply
                }

        # Deterministic Fallback Parser
        intent, entities, memories = self.fallback_parse(user_text)
        return {
            "intent": intent,
            "entities": entities,
            "new_memories_learned": memories,
            "reply": ""
        }

    def fallback_parse(self, text: str) -> Tuple[str, Dict[str, Any], List[Dict[str, Any]]]:
        t_lower = text.lower()
        entities = {}
        learned_memories = []

        # Detect Queries
        if any(q in t_lower for q in ["workspace", "workspaces", "all the works"]):
            return "QUERY_WORKSPACES", entities, learned_memories

        if any(q in t_lower for q in ["all my goals", "all goals", "list goals", "my goals", "what are my goals"]):
            return "QUERY_GOALS", entities, learned_memories

        if any(q in t_lower for q in ["all events", "list events", "my events", "events stream"]):
            return "QUERY_EVENTS", entities, learned_memories

        if any(q in t_lower for q in ["all tasks", "list tasks", "my tasks", "pending tasks", "todos"]):
            return "QUERY_TASKS", entities, learned_memories

        if any(q in t_lower for q in ["all memories", "list memories", "my memories"]):
            return "QUERY_MEMORIES", entities, learned_memories

        # Detect Self-Learning Preferences
        pref_triggers = ["i prefer", "i like", "i hate", "don't remind", "always", "never", "remember that"]
        for tr in pref_triggers:
            if tr in t_lower:
                learned_memories.append({
                    "memory_type": "PREFERENCE" if "prefer" in tr or "like" in tr else "HABIT",
                    "category": "general",
                    "fact": text
                })
                break

        # Goal mutations
        if "delete goal" in t_lower or "remove goal" in t_lower:
            clean_title = re.sub(r"(delete|remove)\s+goal\s*", "", t_lower).strip()
            entities["goal_title"] = clean_title or text
            return "DELETE_GOAL", entities, learned_memories

        if "add goal" in t_lower or "create goal" in t_lower or "new goal" in t_lower:
            clean_title = re.sub(r"(add|create|new)\s+goal\s*", "", t_lower).strip()
            entities["goal_title"] = clean_title or text
            return "CREATE_GOAL", entities, learned_memories

        if "delete task" in t_lower or "remove task" in t_lower:
            clean_title = re.sub(r"(delete|remove)\s+task\s*", "", t_lower).strip()
            entities["task_title"] = clean_title or text
            return "DELETE_TASK", entities, learned_memories

        if "delete memory" in t_lower or "forget memory" in t_lower:
            clean_fact = re.sub(r"(delete|forget)\s+(memory|that)?\s*", "", t_lower).strip()
            entities["memory_fact"] = clean_fact or text
            return "DELETE_MEMORY", entities, learned_memories

        weight_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:kg|kilos|pounds|lbs)", t_lower)
        if "weight" in t_lower or weight_match or "weigh" in t_lower:
            if weight_match:
                entities["weight_kg"] = float(weight_match.group(1))
            return "LOG_WEIGHT", entities, learned_memories

        study_keywords = ["study", "studied", "learning", "revised", "read", "sql", "dbms", "lecture", "assignment"]
        if any(k in t_lower for k in study_keywords):
            dur_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:hours|hrs|hr|hour|mins|minutes)", t_lower)
            if dur_match:
                val = float(dur_match.group(1))
                entities["duration_hours"] = round(val / 60.0, 2) if "min" in dur_match.group(0) else val
            else:
                entities["duration_hours"] = 1.0

            if "sql" in t_lower:
                entities["subject"] = "SQL Joins & Queries"
            elif "dbms" in t_lower:
                entities["subject"] = "DBMS"
            else:
                entities["subject"] = "General Learning"
            return "LOG_STUDY", entities, learned_memories

        workout_keywords = ["workout", "gym", "cardio", "ran", "running", "exercise", "steps", "pushups"]
        if any(k in t_lower for k in workout_keywords):
            entities["workout_type"] = "Cardio & Fitness"
            entities["duration_hours"] = 0.5
            return "LOG_WORKOUT", entities, learned_memories

        task_keywords = ["remind", "reminder", "task", "todo", "schedule"]
        if any(k in t_lower for k in task_keywords):
            entities["task_title"] = text
            return "CREATE_TASK", entities, learned_memories

        if "morning" in t_lower or "briefing" in t_lower or "hello" in t_lower or "hi" in t_lower:
            return "MORNING_BRIEFING", entities, learned_memories

        intent = "LEARN_PREFERENCE" if learned_memories else "GENERAL_CHAT"
        return intent, entities, learned_memories
