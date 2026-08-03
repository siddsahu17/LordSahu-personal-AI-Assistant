import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class DailyPlannerModel(Base):
    """
    Canonical DailyPlanner Model for LordSahu V1.4.
    Represents intelligent daily agendas with day boundary configuration.
    """
    __tablename__ = "daily_planners"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, default="default_user")
    date = Column(String, nullable=False)                         # YYYY-MM-DD
    scope = Column(String, default="daily")                       # daily, weekly, monthly
    status = Column(String, default="active")                     # active, archived
    created_by = Column(String, default="user")                   # ai, user
    day_boundary_time = Column(String, default="06:00")            # Configurable day boundary (e.g. 06:00)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class PlannerItemModel(Base):
    """
    PlannerItem Model representing individual agenda tasks.
    Supports start/end times, repeat rules, attribution, and bidirectional LifeEntry linking.
    """
    __tablename__ = "planner_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    planner_id = Column(String, ForeignKey("daily_planners.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="medium")                    # low, medium, high
    status = Column(String, default="pending")                     # pending, in_progress, completed, skipped, deferred
    start_time = Column(String, nullable=True)                     # e.g. "18:00"
    end_time = Column(String, nullable=True)                       # e.g. "19:30"
    estimated_duration = Column(String, nullable=True)             # e.g. "45 mins"
    repeat_rule = Column(String, nullable=True)                    # daily, weekdays, weekly, monthly, custom
    planner_source = Column(String, default="user")                # ai, user, carry_forward, recurring, template
    completion_source = Column(String, nullable=True)             # manual, life_entry, calendar, ai
    domains = Column(Text, default='["personal"]')                 # JSON array string e.g. ["learning", "projects"]
    related_life_entry_ids = Column(Text, default='[]')            # JSON array of satisfied LifeEntry IDs
    order_index = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class PlannerTemplateModel(Base):
    """
    PlannerTemplate Model for instant task list generation (e.g. Gym Day, Study Day).
    """
    __tablename__ = "planner_templates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, default="default_user")
    name = Column(String, nullable=False)                         # Gym Day, Study Day, Interview Day
    description = Column(Text, nullable=True)
    items_json = Column(Text, nullable=False, default='[]')        # JSON array string of template tasks
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class LifeEntryModel(Base):
    """
    Canonical LifeEntry Model for LordSahu V1 AI Daily Journal & Daily Chronicle.
    Stores every personal life event (weight, workout, expense, study topic, lecture, feature, journal).
    """
    __tablename__ = "life_entries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, default="default_user")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    domains = Column(Text, nullable=False, default='["personal"]')  # JSON array string e.g. ["learning", "projects"]
    category = Column(String, nullable=False, default="journal")   # weight, workout, concept, expense, lecture, feature, journal, photo
    title = Column(String, nullable=False)
    raw_text = Column(Text, nullable=False)
    source_raw_transcript = Column(Text, nullable=True)             # Exact unparsed voice/speech transcript
    structured_data = Column(Text, nullable=True)                  # JSON string payload
    ai_summary = Column(Text, nullable=True)                       # AI generated summary
    confidence = Column(Float, default=1.0)                         # Confidence score (0.0 - 1.0)
    source = Column(String, default="text")                        # voice, text, import, image, api
    entry_status = Column(String, default="active")                # active, edited, deleted
    attachments = Column(Text, nullable=True)                      # JSON array of file/media URIs
    tags = Column(Text, nullable=True)                             # JSON array of tags (auto + manual)
    related_entry_ids = Column(Text, nullable=True)                # JSON array of related entry IDs
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

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
