from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# --- Event Schemas ---
class EventEntity(BaseModel):
    type: str
    value: Any

class EventBase(BaseModel):
    workspace_id: str = "personal"
    source: str = "chat_text"
    event_type: str
    intent: Optional[str] = None
    entities: List[Dict[str, Any]] = []
    payload: Dict[str, Any] = {}
    confidence: float = 1.0
    created_by: str = "system"
    parent_event_id: Optional[str] = None
    related_goal_id: Optional[str] = None
    attachments: List[Dict[str, Any]] = []

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    version: int

    class Config:
        from_attributes = True

# --- Memory Schemas ---
class MemoryCreate(BaseModel):
    memory_type: str = "FACT"  # PREFERENCE, FACT, RELATIONSHIP, GOAL, HABIT, TEMPORAL
    category: str = "general"
    fact: str
    relationship_entity: Optional[str] = None
    confidence: float = 1.0
    source_event_id: Optional[str] = None

class MemoryResponse(MemoryCreate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Goal Schemas ---
class Milestone(BaseModel):
    id: str
    title: str
    completed: bool = False
    target: Optional[float] = None
    current: float = 0.0

class GoalCreate(BaseModel):
    workspace_id: str = "learning"
    title: str
    description: Optional[str] = None
    priority: str = "MEDIUM"
    deadline: Optional[datetime] = None
    status: str = "IN_PROGRESS"
    target_metric: Optional[str] = None
    target_value: Optional[float] = None
    manual_progress: Optional[float] = None
    milestones: List[Dict[str, Any]] = []
    dependencies: List[str] = []
    tags: List[str] = []
    metadata_json: Dict[str, Any] = {}

class GoalResponse(GoalCreate):
    id: str
    user_id: str
    inferred_progress: float = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Task Schemas ---
class TaskCreate(BaseModel):
    workspace_id: str = "personal"
    title: str
    due_date: Optional[datetime] = None
    priority: str = "MEDIUM"
    status: str = "PENDING"
    recurring_rule: Optional[str] = None
    related_goal_id: Optional[str] = None

class TaskResponse(TaskCreate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Knowledge Doc Schemas ---
class KnowledgeDocCreate(BaseModel):
    workspace_id: str = "personal"
    title: str
    doc_type: str = "notes"
    content: str
    metadata_json: Dict[str, Any] = {}

class KnowledgeDocResponse(KnowledgeDocCreate):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Chat & Core Intelligence Orchestration Schemas ---
class ChatMessageCreate(BaseModel):
    text: str
    mode: str = "assistant"  # assistant, coach, focus, reflection, planner, reviewer
    workspace_id: Optional[str] = "personal"
    audio_data: Optional[str] = None  # Base64 or voice recording reference

class ChatResponse(BaseModel):
    id: str
    sender: str
    mode: str
    text: str
    intent: Optional[str] = None
    extracted_entities: List[Dict[str, Any]] = []
    generated_events: List[Dict[str, Any]] = []
    memories_retrieved: List[str] = []
    tasks_created: List[Dict[str, Any]] = []
    voice_audio_base64: Optional[str] = None
    created_at: datetime

# --- Analytics Response Schemas ---
class AnalyticsSummary(BaseModel):
    consistency_score: float
    momentum_index: float
    goal_velocity: float
    burnout_risk_score: float
    learning_efficiency: float
    workout_consistency: float
    total_study_hours: float
    latest_weight_kg: Optional[float]
    weight_trend_kg: List[Dict[str, Any]]
    activity_heatmap: List[Dict[str, Any]]
    focus_hours_today: float

# --- Mission Control Briefing Schema ---
class MorningBriefing(BaseModel):
    user_name: str = "Siddhant"
    greeting: str
    sleep_hours: float
    current_weight: Optional[float]
    top_priority_today: str
    active_goals_summary: List[Dict[str, Any]]
    coach_advice: str
