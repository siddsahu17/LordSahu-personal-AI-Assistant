import re
from typing import Dict, Any, List, Tuple

VALID_INTENTS = {
    "QUERY_WORKSPACES", "QUERY_GOALS", "QUERY_EVENTS", "QUERY_TASKS", "QUERY_MEMORIES",
    "CREATE_GOAL", "DELETE_GOAL", "CREATE_TASK", "DELETE_TASK", "DELETE_MEMORY",
    "LOG_WEIGHT", "LOG_WORKOUT", "LOG_SPORT", "LOG_MEAL", "LOG_WATER", "LOG_SLEEP", "LOG_PR",
    "LOG_STUDY", "LOG_CONCEPT", "LOG_PROBLEM", "LOG_JOB_APP", "LOG_RESUME", "LOG_LECTURE",
    "LOG_ASSIGNMENT", "LOG_EXPENSE", "LOG_INCOME", "LOG_JOURNAL", "LOG_MOOD", "LOG_FEATURE", "LOG_BUG_FIX",
    "MORNING_BRIEFING", "LEARN_PREFERENCE", "GENERAL_CHAT"
}

class ResponseValidator:
    """
    AI Response Validator ensuring LLM JSON outputs adhere strictly to schema specs.
    Includes fallback parsing across all 7 LordSahu Workspace SDK Modules.
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

        # Queries
        if any(q in t_lower for q in ["workspace", "workspaces", "all the works"]):
            return "QUERY_WORKSPACES", entities, learned_memories
        if any(q in t_lower for q in ["all my goals", "all goals", "list goals"]):
            return "QUERY_GOALS", entities, learned_memories

        # LIM (Learning)
        if "learned" in t_lower or "concept" in t_lower:
            entities["concept_name"] = text.replace("today i learned", "").replace("learned", "").strip() or text
            return "LOG_CONCEPT", entities, learned_memories
        if "leetcode" in t_lower or "solved" in t_lower:
            entities["problem_title"] = text
            return "LOG_PROBLEM", entities, learned_memories

        # CIM (Career)
        if "applied to" in t_lower or "job app" in t_lower:
            comp = re.search(r"applied to\s+([a-[#a-zA-Z\s]+)", t_lower)
            entities["company_name"] = comp.group(1).title() if comp else "Target Company"
            return "LOG_JOB_APP", entities, learned_memories
        if "resume" in t_lower:
            entities["summary"] = text
            return "LOG_RESUME", entities, learned_memories

        # Finance
        if "spent" in t_lower or "paid" in t_lower or "rupees" in t_lower or "₹" in t_lower or "dollars" in t_lower or "$" in t_lower:
            amt_match = re.search(r"(?:₹|\$|rs\.?|spent|paid)\s*(\d+(?:\.\d+)?)", t_lower)
            entities["amount"] = float(amt_match.group(1)) if amt_match else 100.0
            entities["description"] = text
            return "LOG_EXPENSE", entities, learned_memories

        # College
        if "lecture" in t_lower or "attended" in t_lower or "class" in t_lower:
            entities["subject"] = "DBMS" if "dbms" in t_lower else "Academic Lecture"
            return "LOG_LECTURE", entities, learned_memories

        # Projects
        if "implemented" in t_lower or "feature" in t_lower or "refactored" in t_lower:
            entities["feature_name"] = text
            return "LOG_FEATURE", entities, learned_memories
        if "fixed bug" in t_lower or "debugged" in t_lower:
            entities["bug_summary"] = text
            return "LOG_BUG_FIX", entities, learned_memories

        # Fitness Intelligence
        weight_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:kg|kilos)", t_lower)
        if "weight" in t_lower or weight_match:
            if weight_match:
                entities["weight_kg"] = float(weight_match.group(1))
            return "LOG_WEIGHT", entities, learned_memories

        workout_keywords = ["workout", "gym", "chest day", "leg day", "arm day", "back day"]
        if any(k in t_lower for k in workout_keywords):
            entities["workout_type"] = "Chest Day" if "chest" in t_lower else "General Workout"
            return "LOG_WORKOUT", entities, learned_memories

        # Default Study
        study_keywords = ["study", "studied", "learning", "revised", "sql", "dbms"]
        if any(k in t_lower for k in study_keywords):
            entities["subject"] = "SQL Joins & Queries" if "sql" in t_lower else "General Learning"
            entities["duration_hours"] = 1.0
            return "LOG_STUDY", entities, learned_memories

        return "GENERAL_CHAT", entities, learned_memories
