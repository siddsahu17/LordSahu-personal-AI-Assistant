import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.repositories.goal_repository import GoalRepository
from app.repositories.event_repository import EventRepository
from app.repositories.memory_repository import MemoryRepository
from app.repositories.task_repository import TaskRepository
from app.schemas import EventCreate, GoalCreate, TaskCreate, MemoryCreate
from app.modules.event_engine import EventEngine

AVAILABLE_WORKSPACES = [
    {"id": "learning", "name": "Learning", "description": "DBMS, SQL, Programming, Courses"},
    {"id": "fitness", "name": "Fitness & Health", "description": "Weight Loss, Workouts, Nutrition"},
    {"id": "career", "name": "Career", "description": "Projects, Internships, Resume, Industry"},
    {"id": "college", "name": "College", "description": "Assignments, Exams, Academics, GPA"},
    {"id": "finance", "name": "Finance", "description": "Budget, Expenses, Savings"},
    {"id": "projects", "name": "Projects", "description": "Software Engineering & AI OS"},
    {"id": "personal", "name": "Personal", "description": "Habits, Journal, Daily Reminders"}
]

class BaseCapability:
    def execute(self, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        raise NotImplementedError

class QueryCapability(BaseCapability):
    def __init__(self, db: Session):
        self.goal_repo = GoalRepository(db)
        self.event_repo = EventRepository(db)
        self.task_repo = TaskRepository(db)
        self.memory_repo = MemoryRepository(db)

    def execute(self, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str, intent: str) -> Dict[str, Any]:
        if intent == "QUERY_WORKSPACES":
            lines = ["Here are your active workspaces in LordSahu AI Personal OS:"]
            for i, w in enumerate(AVAILABLE_WORKSPACES, 1):
                lines.append(f"{i}. **{w['name']}** (`{w['id']}`): {w['description']}")
            return {"reply": "\n".join(lines), "events": [], "tasks": []}

        if intent == "QUERY_GOALS":
            goals = self.goal_repo.list_goals(user_id, workspace_id=workspace_id)
            if not goals:
                return {"reply": "You currently have no active goals in your database. Add one anytime e.g. 'Add goal to learn Rust'!", "events": [], "tasks": []}
            lines = [f"Here are your active living goals in your database ({len(goals)} total):"]
            for g in goals:
                lines.append(f"• **{g.title}** [{g.workspace_id.upper()}]\n  - Target Metric: {g.target_metric or 'custom'} | Priority: {g.priority} | Status: {g.status}")
            return {"reply": "\n\n".join(lines), "events": [], "tasks": []}

        if intent == "QUERY_EVENTS":
            events = self.event_repo.query_events(user_id=user_id, limit=10)
            if not events:
                return {"reply": "No life events logged in your Event Store yet.", "events": [], "tasks": []}
            lines = [f"Here are your recent life events recorded in your Event Store ({len(events)} recent):"]
            for e in events:
                date_str = e.created_at.strftime("%b %d %H:%M") if e.created_at else ''
                lines.append(f"• **{e.event_type}** [{e.workspace_id.upper()}] - {date_str}")
            return {"reply": "\n".join(lines), "events": [], "tasks": []}

        if intent == "QUERY_TASKS":
            tasks = self.task_repo.list_tasks(user_id=user_id, status="PENDING")
            if not tasks:
                return {"reply": "You have no pending tasks in your database.", "events": [], "tasks": []}
            lines = [f"Here are your pending tasks ({len(tasks)} total):"]
            for t in tasks:
                lines.append(f"• **{t.title}** (Priority: {t.priority})")
            return {"reply": "\n".join(lines), "events": [], "tasks": []}

        if intent == "QUERY_MEMORIES":
            memories = self.memory_repo.list_memories(user_id=user_id)
            if not memories:
                return {"reply": "No memory facts stored in your database yet.", "events": [], "tasks": []}
            lines = [f"Here are your stored memory facts ({len(memories)} total):"]
            for m in memories:
                lines.append(f"• [{m.memory_type}] {m.fact}")
            return {"reply": "\n".join(lines), "events": [], "tasks": []}

        return {"reply": "", "events": [], "tasks": []}

class GoalCapability(BaseCapability):
    def __init__(self, db: Session):
        self.db = db
        self.goal_repo = GoalRepository(db)
        self.event_engine = EventEngine(db)

    def create_goal(self, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        g_title = entities.get("goal_title") or entities.get("title") or user_text
        g_ws = entities.get("workspace_id") or workspace_id
        g_target = float(entities.get("target_value") or 20.0)

        g_obj = GoalCreate(title=g_title, workspace_id=g_ws, target_value=g_target)
        db_goal = self.goal_repo.add(self.goal_repo.model_cls(
            user_id=user_id, workspace_id=g_ws, title=g_title, target_value=g_target, target_metric="hours", priority="HIGH"
        ))

        evt = self.event_engine.create_event(EventCreate(
            workspace_id=g_ws, source="chat_text", event_type="GOAL_CREATED", intent="CREATE_GOAL",
            entities=[{"type": "goal_title", "value": g_title}], payload={"goal_id": db_goal.id, "title": g_title}
        ))
        return {
            "reply": f"Living Goal Engine: Added goal '{g_title}' to database.",
            "events": [{"id": evt.id, "type": "GOAL_CREATED", "title": g_title}],
            "tasks": []
        }

    def delete_goal(self, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        g_title = entities.get("goal_title") or entities.get("title") or user_text
        goal = self.goal_repo.find_by_title_or_id(user_id, g_title)
        if goal:
            deleted_title = goal.title
            self.goal_repo.delete(goal)
            evt = self.event_engine.create_event(EventCreate(
                workspace_id=workspace_id, source="chat_text", event_type="GOAL_DELETED", intent="DELETE_GOAL",
                entities=[{"type": "goal_title", "value": deleted_title}], payload={"title": deleted_title}
            ))
            return {
                "reply": f"Living Goal Engine: Deleted goal '{deleted_title}' from database.",
                "events": [{"id": evt.id, "type": "GOAL_DELETED", "title": deleted_title}],
                "tasks": []
            }
        return {"reply": f"Could not find goal matching '{g_title}' to delete.", "events": [], "tasks": []}

class TaskCapability(BaseCapability):
    def __init__(self, db: Session):
        self.task_repo = TaskRepository(db)
        self.event_engine = EventEngine(db)

    def create_task(self, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        t_title = entities.get("task_title") or user_text
        db_task = self.task_repo.add(self.task_repo.model_cls(user_id=user_id, workspace_id=workspace_id, title=t_title, priority="HIGH"))
        evt = self.event_engine.create_event(EventCreate(
            workspace_id=workspace_id, source="chat_text", event_type="TASK_CREATED", intent="CREATE_TASK",
            entities=[{"type": "task_title", "value": t_title}], payload={"task_id": db_task.id, "title": t_title}
        ))
        return {
            "reply": f"Task Engine: Scheduled task '{t_title}'.",
            "events": [{"id": evt.id, "type": "TASK_CREATED", "title": t_title}],
            "tasks": [{"id": db_task.id, "title": db_task.title}]
        }

    def delete_task(self, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        t_title = entities.get("task_title") or user_text
        task = self.task_repo.find_by_title_or_id(user_id, t_title)
        if task:
            deleted_title = task.title
            self.task_repo.delete(task)
            return {"reply": f"Task Engine: Deleted task '{deleted_title}'.", "events": [], "tasks": []}
        return {"reply": f"Could not find task matching '{t_title}'.", "events": [], "tasks": []}

class FitnessCapability(BaseCapability):
    def __init__(self, db: Session):
        self.event_engine = EventEngine(db)
        self.memory_repo = MemoryRepository(db)

    def log_weight(self, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        w_val = entities.get("weight_kg")
        if w_val:
            evt = self.event_engine.create_event(EventCreate(
                workspace_id="fitness", source="chat_text", event_type="WEIGHT_LOGGED", intent="LOG_WEIGHT",
                entities=[{"type": "weight_kg", "value": w_val}], payload={"weight_kg": w_val, "raw_input": user_text}
            ))
            self.memory_repo.add(self.memory_repo.model_cls(
                user_id=user_id, workspace_id="fitness", memory_type="FACT", category="fitness", fact=f"Current body weight recorded as {w_val} kg"
            ))
            return {"reply": f"Recorded {w_val} kg into database Event Store.", "events": [{"id": evt.id, "type": "WEIGHT_LOGGED", "weight_kg": w_val}], "tasks": []}
        return {"reply": "Logged weight event into Event Store.", "events": [], "tasks": []}

    def log_workout(self, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        w_type = entities.get("workout_type") or "Workout"
        evt = self.event_engine.create_event(EventCreate(
            workspace_id="fitness", source="chat_text", event_type="WORKOUT_COMPLETED", intent="LOG_WORKOUT",
            entities=[{"type": "workout_type", "value": w_type}], payload={"workout_type": w_type}
        ))
        return {"reply": f"Recorded '{w_type}' session into Event Store.", "events": [{"id": evt.id, "type": "WORKOUT_COMPLETED", "workout_type": w_type}], "tasks": []}

class StudyCapability(BaseCapability):
    def __init__(self, db: Session):
        self.event_engine = EventEngine(db)

    def log_study(self, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        subj = entities.get("subject") or "General Learning"
        dur = float(entities.get("duration_hours") or 1.0)
        evt = self.event_engine.create_event(EventCreate(
            workspace_id="learning", source="chat_text", event_type="STUDY_SESSION", intent="LOG_STUDY",
            entities=[{"type": "subject", "value": subj}, {"type": "duration_hours", "value": dur}],
            payload={"subject": subj, "duration_hours": dur, "notes": user_text}
        ))
        return {
            "reply": f"Recorded {dur} hours of '{subj}' into database Event Store.",
            "events": [{"id": evt.id, "type": "STUDY_SESSION", "subject": subj, "duration_hours": dur}],
            "tasks": []
        }

class CapabilityRegistry:
    """
    Capability Registry resolving capabilities cleanly by intent.
    Replaces monolithic if-else orchestrator dispatch blocks.
    """
    def __init__(self, db: Session):
        self.db = db
        self.query_cap = QueryCapability(db)
        self.goal_cap = GoalCapability(db)
        self.task_cap = TaskCapability(db)
        self.fitness_cap = FitnessCapability(db)
        self.study_cap = StudyCapability(db)

    def dispatch(self, intent: str, user_id: str, workspace_id: str, entities: Dict[str, Any], user_text: str) -> Dict[str, Any]:
        if intent.startswith("QUERY_"):
            return self.query_cap.execute(user_id, workspace_id, entities, user_text, intent)

        if intent == "CREATE_GOAL":
            return self.goal_cap.create_goal(user_id, workspace_id, entities, user_text)
        if intent == "DELETE_GOAL":
            return self.goal_cap.delete_goal(user_id, workspace_id, entities, user_text)

        if intent == "CREATE_TASK":
            return self.task_cap.create_task(user_id, workspace_id, entities, user_text)
        if intent == "DELETE_TASK":
            return self.task_cap.delete_task(user_id, workspace_id, entities, user_text)

        if intent == "LOG_WEIGHT":
            return self.fitness_cap.log_weight(user_id, workspace_id, entities, user_text)
        if intent == "LOG_WORKOUT":
            return self.fitness_cap.log_workout(user_id, workspace_id, entities, user_text)

        if intent == "LOG_STUDY":
            return self.study_cap.log_study(user_id, workspace_id, entities, user_text)

        return {"reply": "", "events": [], "tasks": []}
