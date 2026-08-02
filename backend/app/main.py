import os
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
                db_ws = WorkspaceModel(**w)
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

# --- Chat & Core Intelligence Endpoint ---
@app.post("/api/chat", response_model=ChatResponse)
def handle_chat(payload: ChatMessageCreate, db: Session = Depends(get_db)):
    orchestrator = CoreOrchestrator(db)
    return orchestrator.process_message(payload)

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

    # Morning briefing structure
    morning_briefing = {
        "user_name": "Siddhant",
        "greeting": f"Good morning Siddhant.",
        "sleep_hours": 7.0,
        "current_weight_kg": context["current_weight_kg"] or 96.8,
        "top_priority_today": "DBMS & SQL Joins Assignment",
        "coach_advice": "Your consistency is up 18%! Focus on your DBMS assignment today.",
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
    return event_eng.query_events(workspace_id=workspace_id, event_type=event_type, search_query=search)

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
            "relationship_entity": m.relationship_entity,
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
