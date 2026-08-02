import re
from typing import Dict, Any, List

class ExecutionPlanner:
    """
    ExecutionPlanner generating multi-step tool execution plans.
    Translates validated intents and entities into structured Tool steps across all 7 Workspace SDK Modules.
    """
    def plan(self, validated_llm_result: Dict[str, Any], user_text: str) -> List[Dict[str, Any]]:
        plan_steps = []
        intent = validated_llm_result.get("intent", "GENERAL_CHAT")
        entities = validated_llm_result.get("entities", {})

        # Learning Intelligence Module (LIM)
        if intent == "LOG_CONCEPT":
            plan_steps.append({
                "tool": "log_concept",
                "params": {"concept_name": entities.get("concept_name") or user_text, "subject": entities.get("subject") or "Learning"}
            })
        elif intent == "LOG_PROBLEM":
            plan_steps.append({
                "tool": "log_problem",
                "params": {"problem_title": entities.get("problem_title") or user_text, "difficulty": entities.get("difficulty") or "Medium"}
            })

        # Career Intelligence Module (CIM)
        elif intent == "LOG_JOB_APP":
            plan_steps.append({
                "tool": "log_job_app",
                "params": {"company_name": entities.get("company_name") or "Company", "role_title": entities.get("role_title") or "AI Engineer"}
            })
        elif intent == "LOG_RESUME":
            plan_steps.append({
                "tool": "log_resume",
                "params": {"summary": entities.get("summary") or user_text}
            })

        # College Intelligence Module
        elif intent == "LOG_LECTURE":
            plan_steps.append({
                "tool": "log_lecture",
                "params": {"subject": entities.get("subject") or "DBMS", "attended": entities.get("attended", True)}
            })
        elif intent == "LOG_ASSIGNMENT":
            plan_steps.append({
                "tool": "log_assignment",
                "params": {"title": entities.get("title") or user_text, "subject": entities.get("subject") or "Academics"}
            })

        # Finance Intelligence Module
        elif intent == "LOG_EXPENSE":
            plan_steps.append({
                "tool": "log_expense",
                "params": {
                    "amount": entities.get("amount") or 0.0,
                    "category": entities.get("category") or "General",
                    "description": entities.get("description") or user_text
                }
            })
        elif intent == "LOG_INCOME":
            plan_steps.append({
                "tool": "log_income",
                "params": {"amount": entities.get("amount") or 0.0, "source": entities.get("source") or "Income"}
            })

        # Personal Intelligence Module
        elif intent == "LOG_JOURNAL":
            plan_steps.append({
                "tool": "log_journal",
                "params": {"text": entities.get("text") or user_text, "mood": entities.get("mood") or "Positive"}
            })
        elif intent == "LOG_MOOD":
            plan_steps.append({
                "tool": "log_mood",
                "params": {"mood": entities.get("mood") or "Great"}
            })

        # Project Intelligence Module
        elif intent == "LOG_FEATURE":
            plan_steps.append({
                "tool": "log_feature",
                "params": {"feature_name": entities.get("feature_name") or user_text, "project_name": entities.get("project_name") or "LordSahu AI OS"}
            })
        elif intent == "LOG_BUG_FIX":
            plan_steps.append({
                "tool": "log_bug_fix",
                "params": {"bug_summary": entities.get("bug_summary") or user_text}
            })

        # Fitness Intelligence Module (FIM)
        elif intent == "LOG_WEIGHT":
            plan_steps.append({
                "tool": "log_weight",
                "params": {"weight_kg": entities.get("weight_kg") or 0.0}
            })
        elif intent == "LOG_WORKOUT":
            plan_steps.append({
                "tool": "log_workout",
                "params": {"workout_type": entities.get("workout_type") or "Cardio & Fitness"}
            })
        elif intent == "LOG_SPORT":
            plan_steps.append({
                "tool": "log_sport",
                "params": {
                    "sport_name": entities.get("sport_name") or "Football",
                    "duration_mins": entities.get("duration_mins") or 60.0
                }
            })
        elif intent == "LOG_WATER":
            plan_steps.append({
                "tool": "log_water",
                "params": {"liters": entities.get("liters") or 1.0}
            })
        elif intent == "LOG_SLEEP":
            plan_steps.append({
                "tool": "log_sleep",
                "params": {"hours": entities.get("hours") or 7.0}
            })

        # Living OS Goals & Tasks
        elif intent == "CREATE_GOAL":
            plan_steps.append({
                "tool": "create_goal",
                "params": {"title": entities.get("goal_title") or user_text, "target_value": 10.0}
            })
        elif intent == "DELETE_GOAL":
            plan_steps.append({
                "tool": "delete_goal",
                "params": {"title": entities.get("goal_title") or user_text}
            })
        elif intent == "CREATE_TASK":
            plan_steps.append({
                "tool": "create_task",
                "params": {"title": entities.get("task_title") or user_text}
            })
        elif intent == "LOG_STUDY":
            plan_steps.append({
                "tool": "log_study",
                "params": {
                    "subject": entities.get("subject") or "General Learning",
                    "duration_hours": entities.get("duration_hours") or 1.0
                }
            })

        # Calendar Scheduling Interception
        t_lower = user_text.lower()
        if "schedule" in t_lower or "calendar" in t_lower or "tomorrow" in t_lower:
            if not any(step["tool"] == "create_calendar_event" for step in plan_steps):
                plan_steps.append({
                    "tool": "create_calendar_event",
                    "params": {
                        "title": entities.get("goal_title") or entities.get("task_title") or user_text,
                        "start_time": "Tomorrow at 9:00 AM"
                    }
                })

        return plan_steps
