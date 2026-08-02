import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class WorkspaceModel(Base):
    __tablename__ = "workspaces"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class EventModel(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, default="default_user")
    workspace_id = Column(String, nullable=False, default="personal")
    source = Column(String, nullable=False, default="chat_text")
    event_type = Column(String, nullable=False)
    intent = Column(String, nullable=True)
    entities = Column(Text, nullable=True)  # JSON text
    payload = Column(Text, nullable=True)   # JSON text
    confidence = Column(Float, default=1.0)
    created_by = Column(String, default="system")
    parent_event_id = Column(String, nullable=True)
    related_goal_id = Column(String, nullable=True)
    attachments = Column(Text, nullable=True)  # JSON text
    schema_version = Column(String, default="1.0")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class MemoryModel(Base):
    __tablename__ = "memories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, default="default_user")
    workspace_id = Column(String, nullable=False, default="personal")
    memory_type = Column(String, nullable=False, default="FACT")  # PREFERENCE, FACT, RELATIONSHIP, GOAL, HABIT, TEMPORAL
    category = Column(String, nullable=False, default="general")
    fact = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    source_event_id = Column(String, nullable=True)
    last_verified = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_used = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    times_used = Column(Integer, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class GoalModel(Base):
    __tablename__ = "goals"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, default="default_user")
    workspace_id = Column(String, nullable=False, default="personal")
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="MEDIUM")  # HIGH, MEDIUM, LOW
    deadline = Column(DateTime, nullable=True)
    status = Column(String, default="IN_PROGRESS")  # NOT_STARTED, IN_PROGRESS, COMPLETED, ABANDONED
    target_metric = Column(String, nullable=True)   # e.g., "hours", "kg", "tasks"
    target_value = Column(Float, nullable=True)
    manual_progress = Column(Float, nullable=True)
    milestones = Column(Text, nullable=True)        # JSON text
    dependencies = Column(Text, nullable=True)      # JSON text
    tags = Column(Text, nullable=True)              # JSON text
    metadata_json = Column(Text, nullable=True)     # JSON text
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, default="default_user")
    workspace_id = Column(String, nullable=False, default="personal")
    title = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String, default="MEDIUM")
    status = Column(String, default="PENDING")  # PENDING, COMPLETED, CANCELLED
    recurring_rule = Column(String, nullable=True)
    related_goal_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class KnowledgeDocModel(Base):
    __tablename__ = "knowledge_repository"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, default="default_user")
    workspace_id = Column(String, nullable=False, default="personal")
    title = Column(String, nullable=False)
    doc_type = Column(String, default="note")  # pdf, note, markdown, book, resume
    content = Column(Text, nullable=False)
    metadata_json = Column(Text, nullable=True)  # JSON text
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, default="default_user")
    workspace_id = Column(String, default="personal")
    title = Column(String, default="New Conversation")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=True)
    user_id = Column(String, nullable=False, default="default_user")
    sender = Column(String, nullable=False)  # "user" or "lord_sahu"
    mode = Column(String, default="assistant")
    text = Column(Text, nullable=False)
    intent = Column(String, nullable=True)
    extracted_entities = Column(Text, nullable=True)
    generated_events = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
