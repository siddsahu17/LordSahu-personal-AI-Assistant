import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, ForeignKey, Boolean
from app.database import Base

def utc_now():
    return datetime.now(timezone.utc)

def generate_uuid():
    return str(uuid.uuid4())

class EventModel(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, default="default_user", index=True)
    workspace_id = Column(String, default="personal", index=True)
    source = Column(String, default="chat_text")  # chat_text, voice, task_complete, system
    event_type = Column(String, index=True)  # WEIGHT_LOGGED, STUDY_SESSION, WORKOUT_COMPLETED, etc.
    intent = Column(String, nullable=True)
    entities = Column(Text, default="[]")  # JSON string array/object
    payload = Column(Text, default="{}")  # JSON string dict
    confidence = Column(Float, default=1.0)
    created_by = Column(String, default="system")
    parent_event_id = Column(String, nullable=True)
    related_goal_id = Column(String, nullable=True)
    attachments = Column(Text, default="[]")  # JSON string list
    created_at = Column(DateTime(timezone=True), default=utc_now, index=True)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    version = Column(Integer, default=1)

class MemoryModel(Base):
    __tablename__ = "memories"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, default="default_user", index=True)
    memory_type = Column(String, default="FACT", index=True)  # PREFERENCE, FACT, RELATIONSHIP, GOAL, HABIT, TEMPORAL
    category = Column(String, default="general", index=True)  # fitness, learning, schedule, etc.
    fact = Column(Text, nullable=False)
    relationship_entity = Column(String, nullable=True)
    confidence = Column(Float, default=1.0)
    source_event_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class GoalModel(Base):
    __tablename__ = "goals"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, default="default_user", index=True)
    workspace_id = Column(String, default="learning", index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="MEDIUM")  # HIGH, MEDIUM, LOW
    deadline = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="IN_PROGRESS", index=True)  # NOT_STARTED, IN_PROGRESS, COMPLETED, PAUSED
    target_metric = Column(String, nullable=True)  # e.g. "hours", "kg", "sessions", "tasks"
    target_value = Column(Float, nullable=True)  # e.g. 20.0
    manual_progress = Column(Float, nullable=True)  # optional explicit % override
    milestones = Column(Text, default="[]")  # JSON string
    dependencies = Column(Text, default="[]")  # JSON string
    tags = Column(Text, default="[]")  # JSON string
    metadata_json = Column(Text, default="{}")
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, default="default_user", index=True)
    workspace_id = Column(String, default="personal", index=True)
    title = Column(String, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    priority = Column(String, default="MEDIUM")
    status = Column(String, default="PENDING", index=True)  # PENDING, COMPLETED, CANCELLED
    recurring_rule = Column(String, nullable=True)  # DAILY, WEEKLY, etc.
    related_goal_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class KnowledgeDocModel(Base):
    __tablename__ = "knowledge_docs"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, default="default_user", index=True)
    workspace_id = Column(String, default="personal", index=True)
    title = Column(String, nullable=False)
    doc_type = Column(String, default="notes")  # pdf, resume, syllabus, workout_plan, notes
    content = Column(Text, nullable=False)
    metadata_json = Column(Text, default="{}")
    created_at = Column(DateTime(timezone=True), default=utc_now)

class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, default="default_user", index=True)
    sender = Column(String, nullable=False)  # user, lord_sahu
    mode = Column(String, default="assistant")  # assistant, coach, focus, reflection, planner, reviewer
    text = Column(Text, nullable=False)
    audio_url = Column(String, nullable=True)
    intent = Column(String, nullable=True)
    extracted_entities = Column(Text, nullable=True)  # JSON string
    generated_events = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime(timezone=True), default=utc_now, index=True)

class WorkspaceModel(Base):
    __tablename__ = "workspaces"

    id = Column(String, primary_key=True)  # learning, fitness, career, college, finance, personal
    name = Column(String, nullable=False)
    icon = Column(String, default="folder")
    color = Column(String, default="#6366f1")
    description = Column(Text, nullable=True)
