import os
import json
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db, init_db, SessionLocal
from app.models import WorkspaceModel
from app.schemas import (
    ChatMessageCreate, ChatResponse, GoalCreate, EventCreate,
    TaskCreate, KnowledgeDocCreate, MemoryCreate
)
from app.modules.core_orchestrator import CoreOrchestrator
from app.modules.context_engine import ContextEngine
from app.modules.goal_engine import GoalEngine
from app.modules.event_engine import EventEngine
from app.modules.task_engine import TaskEngine
from app.modules.knowledge_engine import KnowledgeEngine
from app.modules.memory_engine import MemoryEngine
from app.modules.analytics_engine import AnalyticsEngine
from app.modules.report_generator import ReportGenerator

DEFAULT_WORKSPACES = [
    {"id": "learning", "name": "Learning", "icon": "book-open", "color": "#3b82f6", "description": "SQL, DBMS, Programming & Courses"},
    {"id": "fitness", "name": "Fitness & Health", "icon": "activity", "color": "#10b981", "description": "Weight, Cardio, Gym & Nutrition"},
    {"id": "career", "name": "Career", "icon": "briefcase", "color": "#8b5cf6", "description": "Jobs, Internships & Resume"},
    {"id": "college", "name": "College", "icon": "graduation-cap", "color": "#f59e0b", "description": "Semester 5, Exams & Labs"},
    {"id": "finance", "name": "Finance", "icon": "dollar-sign", "color": "#ec4899", "description": "Expenses & Budgeting"},
    {"id": "projects", "name": "Projects", "icon": "code", "color": "#6366f1", "description": "LordSahu AI OS & Software"},
    {"id": "personal", "name": "Personal", "icon": "user", "color": "#14b8a6", "description": "Journaling & Daily Life"}
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema
    init_db()
    # Seed default workspaces if empty
    db = SessionLocal()
    try:
        count = db.query(WorkspaceModel).count()
        if count == 0:
            for w in DEFAULT_WORKSPACES:
                db_ws = WorkspaceModel(
                    id=w["id"],
                    name=w["name"],
                    slug=w["id"],
                    description=w.get("description", "")
                )
                db.add(db_ws)
            db.commit()
    finally:
        db.close()
    yield

app = FastAPI(
    title="LordSahu AI Personal Operating System API",
    version="0.1.0",
    lifespan=lifespan
)

# Ensure DB tables exist on import
init_db()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "online", "system": "LordSahu AI OS", "version": "0.1.0"}

# --- Chat & Core Intelligence Endpoints ---
@app.post("/api/chat", response_model=ChatResponse)
def handle_chat(payload: ChatMessageCreate, db: Session = Depends(get_db)):
    orchestrator = CoreOrchestrator(db)
    return orchestrator.process_message(payload)

@app.get("/api/chat/history")
def get_chat_history(user_id: str = "default_user", session_id: Optional[str] = None, db: Session = Depends(get_db)):
    from app.repositories.chat_repository import ChatRepository
    chat_repo = ChatRepository(db)
    messages = chat_repo.list_messages(user_id=user_id, session_id=session_id, limit=50)
    return [
        {
            "id": m.id,
            "sender": m.sender,
            "mode": m.mode,
            "text": m.text,
            "intent": m.intent,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
        for m in messages
    ]

# --- Mission Control Dashboard Endpoint ---
@app.get("/api/dashboard")
def get_dashboard(user_id: str = "default_user", db: Session = Depends(get_db)):
    ctx_engine = ContextEngine(db, user_id)
    goal_eng = GoalEngine(db, user_id)
    event_eng = EventEngine(db, user_id)
    analytics_eng = AnalyticsEngine(db, user_id)

    context = ctx_engine.build_context()
    goals = goal_eng.list_goals()
    analytics = analytics_eng.compute_analytics()
    recent_events = event_eng.query_events(limit=10)

    # Briefing structure generated directly from real DB context
    morning_briefing = {
        "user_name": "Siddhant",
        "greeting": "Good morning Siddhant.",
        "sleep_hours": 7.0,
        "current_weight_kg": context["current_weight_kg"],
        "top_priority_today": goals[0]["title"] if goals else "No active goals yet",
        "coach_advice": f"Your Event Store has {len(recent_events)} recent events recorded. Consistency Score: {analytics['consistency_score']}%.",
        "goals_summary": goals
    }

    return {
        "briefing": morning_briefing,
        "analytics": analytics,
        "goals": goals,
        "recent_events": recent_events,
        "context": context
    }

# --- Goals Endpoints ---
@app.get("/api/goals")
def list_goals(workspace_id: str = Query("all"), db: Session = Depends(get_db)):
    goal_eng = GoalEngine(db)
    return goal_eng.list_goals(workspace_id=workspace_id)

@app.post("/api/goals")
def create_goal(payload: GoalCreate, db: Session = Depends(get_db)):
    goal_eng = GoalEngine(db)
    goal = goal_eng.create_goal(payload)
    return {"status": "success", "id": goal.id}

# --- Tasks Endpoints ---
@app.get("/api/tasks")
def list_tasks(workspace_id: str = Query("all"), status: str = Query(None), db: Session = Depends(get_db)):
    task_eng = TaskEngine(db)
    return task_eng.list_tasks(workspace_id=workspace_id, status=status)

@app.post("/api/tasks")
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task_eng = TaskEngine(db)
    t = task_eng.create_task(payload)
    return {"status": "success", "id": t.id}

@app.patch("/api/tasks/{task_id}")
def update_task_status(task_id: str, new_status: str = Query(...), db: Session = Depends(get_db)):
    task_eng = TaskEngine(db)
    res = task_eng.update_task_status(task_id, new_status)
    if not res:
        raise HTTPException(status_code=404, detail="Task not found")
    return res

# --- Event Store & Life Timeline Endpoints ---
@app.get("/api/events")
def list_events(workspace_id: str = Query("all"), event_type: str = Query("all"), search: str = Query(None), db: Session = Depends(get_db)):
    event_eng = EventEngine(db)
    return event_eng.query_events(workspace_id=workspace_id, event_type=event_type, search=search)

@app.post("/api/events")
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    event_eng = EventEngine(db)
    evt = event_eng.create_event(payload)
    return {"status": "success", "id": evt.id}

@app.get("/api/timeline")
def get_timeline(search: str = Query(None), db: Session = Depends(get_db)):
    event_eng = EventEngine(db)
    return event_eng.get_life_timeline(search_query=search)

# --- Memories Endpoints ---
@app.get("/api/memories")
def list_memories(memory_type: str = Query(None), category: str = Query(None), db: Session = Depends(get_db)):
    mem_eng = MemoryEngine(db)
    memories = mem_eng.list_memories(memory_type=memory_type, category=category)
    return [
        {
            "id": m.id,
            "memory_type": m.memory_type,
            "category": m.category,
            "fact": m.fact,
            "confidence": m.confidence,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
        for m in memories
    ]

@app.post("/api/memories")
def add_memory(payload: MemoryCreate, db: Session = Depends(get_db)):
    mem_eng = MemoryEngine(db)
    m = mem_eng.add_memory(payload)
    return {"status": "success", "id": m.id}

# --- Daily Planner V1.4 Endpoints ---
@app.get("/api/planner/today")
def get_today_planner(user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.modules.daily_planner_engine import DailyPlannerEngine
    engine = DailyPlannerEngine(db, user_id)
    return engine.get_today_planner()

@app.post("/api/planner/items")
def add_planner_item(payload: Dict[str, Any], user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.modules.daily_planner_engine import DailyPlannerEngine
    engine = DailyPlannerEngine(db, user_id)
    return engine.add_item_to_today(
        title=payload.get("title", "New Task"),
        priority=payload.get("priority", "medium"),
        start_time=payload.get("start_time"),
        end_time=payload.get("end_time"),
        estimated_duration=payload.get("estimated_duration"),
        repeat_rule=payload.get("repeat_rule"),
        planner_source=payload.get("planner_source", "user"),
        domains=payload.get("domains", ["personal"])
    )

@app.patch("/api/planner/items/{item_id}")
def update_planner_item(item_id: str, payload: Dict[str, Any], db: Session = Depends(get_db)):
    from app.repositories.daily_planner_repository import DailyPlannerRepository
    repo = DailyPlannerRepository(db)
    res = repo.update_item(item_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Planner item not found")
    return {"status": "success", "item_id": res.id, "new_status": res.status}

@app.delete("/api/planner/items/{item_id}")
def delete_planner_item(item_id: str, db: Session = Depends(get_db)):
    from app.repositories.daily_planner_repository import DailyPlannerRepository
    repo = DailyPlannerRepository(db)
    success = repo.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Planner item not found")
    return {"status": "success", "deleted_item_id": item_id}

@app.post("/api/planner/carry-forward")
def carry_forward_planner(user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.modules.daily_planner_engine import DailyPlannerEngine
    engine = DailyPlannerEngine(db, user_id)
    return engine.carry_forward_unfinished()

@app.post("/api/planner/morning-brief")
def generate_morning_brief(user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.modules.daily_planner_engine import DailyPlannerEngine
    engine = DailyPlannerEngine(db, user_id)
    return engine.generate_morning_brief()

@app.post("/api/planner/evening-shutdown")
def run_evening_shutdown(user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.modules.daily_planner_engine import DailyPlannerEngine
    engine = DailyPlannerEngine(db, user_id)
    return engine.run_evening_shutdown()

@app.get("/api/planner/templates")
def list_planner_templates(user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.repositories.daily_planner_repository import DailyPlannerRepository
    repo = DailyPlannerRepository(db)
    templates = repo.list_templates(user_id)
    return [
        {"id": t.id, "name": t.name, "description": t.description, "items": json.loads(t.items_json) if t.items_json else []}
        for t in templates
    ]

# --- LifeEntry & Daily Chronicle V1 Endpoints ---
@app.get("/api/life-entries")
def list_life_entries(
    domain: str = Query("all"),
    category: str = Query("all"),
    search: str = Query(None),
    status: str = Query("active"),
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    from app.repositories.life_entry_repository import LifeEntryRepository
    repo = LifeEntryRepository(db)
    entries = repo.query_entries(user_id=user_id, domain=domain, category=category, search_query=search, status=status)
    return [
        {
            "id": e.id,
            "timestamp": e.timestamp.strftime("%Y-%m-%d %H:%M:%S") if e.timestamp else "",
            "domains": json.loads(e.domains) if e.domains else [],
            "category": e.category,
            "title": e.title,
            "raw_text": e.raw_text,
            "structured_data": json.loads(e.structured_data) if e.structured_data else {},
            "ai_summary": e.ai_summary,
            "confidence": e.confidence,
            "source": e.source,
            "entry_status": e.entry_status,
            "tags": json.loads(e.tags) if e.tags else []
        }
        for e in entries
    ]

@app.get("/api/daily-chronicle")
def get_daily_chronicle(user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.modules.life_entry_engine import LifeEntryEngine
    engine = LifeEntryEngine(db, user_id)
    return engine.generate_daily_chronicle()

@app.get("/api/life-insights")
def get_life_insights(user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.modules.life_entry_engine import LifeEntryEngine
    engine = LifeEntryEngine(db, user_id)
    return engine.compute_5_core_insights()

@app.get("/api/life-entries/recent-topic")
def get_recent_topic(user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.repositories.life_entry_repository import LifeEntryRepository
    repo = LifeEntryRepository(db)
    return repo.get_recent_active_topic(user_id=user_id)

# --- Workspace SDK Endpoint ---
@app.get("/api/workspace/overview")
def get_workspace_overview(workspace_id: str = Query("learning"), user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.workspaces.workspace_sdk import workspace_sdk
    module = workspace_sdk.get_workspace(workspace_id)
    if not module:
        raise HTTPException(status_code=404, detail=f"Workspace '{workspace_id}' not found in Workspace SDK.")
    return {
        "workspace_id": module.workspace_id,
        "workspace_name": module.workspace_name,
        "overview": module.get_analytics_overview(db, user_id)
    }

# --- Fitness Intelligence Module Endpoint ---
@app.get("/api/fitness/overview")
def get_fitness_overview(user_id: str = "default_user", db: Session = Depends(get_db)):
    from app.modules.fitness_analytics import FitnessAnalyticsEngine
    engine = FitnessAnalyticsEngine(db, user_id)
    return engine.compute_fitness_overview()

# --- Calendar Provider Endpoint ---
@app.get("/api/calendar")
def get_calendar_events():
    from app.services.calendar_provider import calendar_provider
    return calendar_provider.list_upcoming_events()

# --- Knowledge Base Endpoints ---
@app.get("/api/knowledge")
def list_knowledge(workspace_id: str = Query("all"), db: Session = Depends(get_db)):
    k_eng = KnowledgeEngine(db)
    return k_eng.list_documents(workspace_id=workspace_id)

@app.post("/api/knowledge")
def add_knowledge(payload: KnowledgeDocCreate, db: Session = Depends(get_db)):
    k_eng = KnowledgeEngine(db)
    doc = k_eng.add_document(payload)
    return {"status": "success", "id": doc.id}

# --- Reports & Reflection Endpoint ---
@app.get("/api/reports")
def get_reports(timeframe: str = Query("weekly"), db: Session = Depends(get_db)):
    rep_gen = ReportGenerator(db)
    return rep_gen.generate_report(timeframe=timeframe)

# --- Workspaces Endpoint ---
@app.get("/api/workspaces")
def list_workspaces(db: Session = Depends(get_db)):
    return db.query(WorkspaceModel).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
