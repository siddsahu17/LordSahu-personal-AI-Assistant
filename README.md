# 🔮 LordSahu AI Personal Operating System — Complete Codebase Summary & Architecture Handoff

**Version:** 0.1.0  
**Owner:** Siddhant Kumar Sahu  
**Tech Stack:** Python 3.12 (FastAPI, SQLAlchemy, LangChain, SQLite, `uv`) + React 18 / Vite 8 (Vanilla CSS, Neo-Brutalist Design System, Lucide Icons, Recharts, Web STT/TTS).

---

## 🎯 Executive Vision & Core Philosophy

LordSahu is **not** a productivity app, habit tracker, or standard chatbot.  
LordSahu is an **AI Personal Operating System** whose primary interface is **conversation**.

- **Conversation-First Interface:** Zero manual form filling, zero manual spreadsheet updating. The user simply speaks or types, and LordSahu parses intent, extracts entities, and executes database actions automatically.
- **Unified Digital Chief of Staff:** Replaces fragmented apps (health trackers, study logs, goal trackers, reminder tools) with a single intelligent, self-learning persona.
- **Append-Only Life Event Store:** All user activities, study sessions, workouts, and weight logs are stored as immutable events.
- **Typed Dynamic Memories:** Stored facts, preferences, habits, goals, and relationships are automatically updated and retrieved in context on every prompt.

---

## 🏗️ High-Level System Architecture

```
                               ┌───────────────────────────────────────────────┐
                               │               User Interface                  │
                               │        React + Vite (Neo-Brutalism)           │
                               │   STT Voice Input & Female TTS Speech Synthesis│
                               └──────────────────────┬────────────────────────┘
                                                      │ HTTP / REST API
                                                      ▼
                               ┌───────────────────────────────────────────────┐
                               │               FastAPI Server                  │
                               │              (app/main.py)                    │
                               └──────────────────────┬────────────────────────┘
                                                      │
                                                      ▼
                               ┌───────────────────────────────────────────────┐
                               │      Core Intelligence Orchestrator           │
                               │      (app/modules/core_orchestrator.py)       │
                               └──────┬────────────────────────────────┬───────┘
                                      │                                │
                 ┌────────────────────┴──────────┐      ┌──────────────┴──────────────────┐
                 │  LangChain LLM Orchestrator   │      │ Dynamic Context & Memory Bundle │
                 │  (ChatOpenAI reading .env)    │      │ (ContextEngine + MemoryEngine)   │
                 └────────────────────┬──────────┘      └──────────────┬──────────────────┘
                                      │                                │
                                      └────────────────┬───────────────┘
                                                       │
                                                       ▼
                               ┌───────────────────────────────────────────────┐
                               │           SQLite Database Engine              │
                               │                (lordsahu.db)                  │
                               │  [Events, Memories, Goals, Tasks, Messages]   │
                               └───────────────────────────────────────────────┘
```

---

## 📁 Repository Directory Map

```
LordSahu/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI server routes & CORS
│   │   ├── database.py              # SQLAlchemy engine & session factory
│   │   ├── models.py                # SQLAlchemy ORM database models
│   │   ├── schemas.py               # Pydantic v2 validation schemas
│   │   └── modules/
│   │       ├── context_engine.py    # Bundles date, time, goals, events into context
│   │       ├── memory_engine.py     # Typed memories & semantic lookup
│   │       ├── event_engine.py      # Immutable append-only Event Store
│   │       ├── goal_engine.py       # Living Goals & dynamic inferred progress math
│   │       ├── task_engine.py       # Task scheduling & status management
│   │       ├── knowledge_engine.py  # Document storage & RAG keyword matching
│   │       ├── analytics_engine.py  # Consistency Score, Velocity, Burnout Risk, Heatmap
│   │       ├── report_generator.py # Periodic AI reflection review generator
│   │       └── core_orchestrator.py# Main LangChain LLM & self-learning orchestrator
│   ├── tests/
│   │   └── test_backend.py          # Pytest test suite (6/6 passing)
│   ├── .env                         # API Keys (OPENAI_API_KEY)
│   ├── .env.example                 # Environment template
│   ├── pyproject.toml               # Python project & dependencies
│   └── requirements.txt             # Pip manifest for containerization
├── frontend/
│   ├── src/
│   │   ├── api.js                   # REST API client helpers
│   │   ├── App.jsx                  # Main application container & view router
│   │   ├── index.css                # Neo-Brutalist CSS design system & utilities
│   │   └── components/
│   │       ├── Navigation.jsx       # Header bar with Persona Dropdown & Workspace Selector
│   │       ├── LandingPage.jsx      # Hero landing page & OS module cards
│   │       ├── Dashboard.jsx        # Mission Control dashboard view
│   │       ├── Chat.jsx             # Conversational AI interface (STT, TTS, intent tags)
│   │       ├── Goals.jsx            # Living goals view & inferred progress bars
│   │       ├── Timeline.jsx         # Git history style temporal event tree
│   │       ├── Reports.jsx          # AI reflection review cards
│   │       ├── Analytics.jsx        # Visual analytics charts & 14-day activity heatmap
│   │       ├── Settings.jsx         # AI persona & voice settings
│   │       ├── Profile.jsx          # Operator profile stats & streak info
│   │       └── Memories.jsx         # Memory bank viewer
│   ├── package.json                 # Node dependencies
│   └── vite.config.js               # Vite build configuration
└── LORDSAHU_MASTER_BLUEPRINT.md     # Product design & architecture blueprint
```

---

## 🗄️ Database Schemas (SQLAlchemy ORM)

All data is stored strictly in SQLite (`lordsahu.db`):

### 1. `events` (Event Store)
- `id` (String UUID, Primary Key)
- `user_id` (String)
- `workspace_id` (String: `learning`, `fitness`, `career`, `college`, `finance`, `projects`, `personal`)
- `source` (String: `chat_text`, `voice_audio`, `system`)
- `event_type` (String: `WEIGHT_LOGGED`, `STUDY_SESSION`, `WORKOUT_COMPLETED`, `GOAL_CREATED`, `GOAL_DELETED`, `TASK_CREATED`)
- `intent` (String)
- `entities` (JSON text)
- `payload` (JSON text)
- `confidence` (Float)
- `created_by` (String)
- `parent_event_id` (String, Optional)
- `related_goal_id` (String, Optional)
- `attachments` (JSON text)
- `created_at` / `updated_at` (DateTime)

### 2. `memories` (Memory Bank)
- `id` (String UUID)
- `user_id` (String)
- `workspace_id` (String)
- `memory_type` (Enum String: `PREFERENCE`, `FACT`, `RELATIONSHIP`, `GOAL`, `HABIT`, `TEMPORAL`)
- `category` (String)
- `fact` (Text)
- `confidence` (Float)
- `source_event_id` (String, Optional)
- `created_at` / `updated_at` (DateTime)

### 3. `goals` (Living Goals)
- `id` (String UUID)
- `user_id` (String)
- `workspace_id` (String)
- `title` (String)
- `description` (Text)
- `priority` (String: `HIGH`, `MEDIUM`, `LOW`)
- `deadline` (DateTime, Optional)
- `status` (String: `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, `ABANDONED`)
- `target_metric` (String: `hours`, `kg`, `tasks`)
- `target_value` (Float)
- `manual_progress` (Float, Optional)
- `milestones` (JSON text)
- `tags` (JSON text)
- `created_at` / `updated_at` (DateTime)

### 4. `chat_messages` (Chat Stream History)
- `id` (String UUID)
- `user_id` (String)
- `sender` (String: `user`, `lord_sahu`)
- `mode` (String: `assistant`, `coach`, `focus`, `reflection`, `planner`, `reviewer`)
- `text` (Text)
- `intent` (String)
- `extracted_entities` (JSON text)
- `generated_events` (JSON text)
- `created_at` (DateTime)

---

## 🧠 Core Intelligence Orchestrator (`core_orchestrator.py`)

### 1. LangChain LLM Pipeline
- Loads API credentials from `.env` (`OPENAI_API_KEY`, `OPENAI_MODEL_NAME=gpt-4o`, `OPENAI_API_BASE`).
- Passes user context (time/date, weight, active goals, today's events, retrieved memories, persona instructions) into `ChatPromptTemplate`.
- Invokes `ChatOpenAI | JsonOutputParser` to produce structured JSON output.

### 2. Supported Conversational Intents
- **Database Query Intents:**
  - `QUERY_WORKSPACES`: Formats bulleted workspace list (`Learning`, `Fitness`, `Career`, etc.).
  - `QUERY_GOALS`: Formats living goals with inferred progress %.
  - `QUERY_EVENTS`: Formats logged life events.
  - `QUERY_TASKS`: Formats pending tasks.
  - `QUERY_MEMORIES`: Formats stored facts & preferences.
- **Database Mutation Intents:**
  - `CREATE_GOAL`: Creates a new goal in `GoalModel` & logs `GOAL_CREATED` event.
  - `DELETE_GOAL`: Matches title/ID and deletes goal from `GoalModel`.
  - `CREATE_TASK`: Schedules task in `TaskModel`.
  - `DELETE_TASK`: Deletes task from `TaskModel`.
  - `DELETE_MEMORY`: Removes fact from `MemoryModel`.
  - `LOG_WEIGHT`, `LOG_STUDY`, `LOG_WORKOUT`: Creates event & updates memory.

### 3. Self-Learning Feedback Loop
- Evaluates every user input for preferences, schedule choices, or corrections (e.g. *"I prefer studying after 8 PM"*).
- Automatically records extracted insights as `PREFERENCE`, `HABIT`, or `FACT` memories in `MemoryModel`.
- Injects retrieved memories into all subsequent prompts to continuously personalize responses.

---

## 🎨 Frontend Design System (Neo-Brutalism)

The UI adheres strictly to a modern **Neo-Brutalist** design language:
- **Background:** Warm off-white (`#f7f4ed`).
- **Cards:** Pure white (`#ffffff`), 3px solid black border (`border-3 border-black`), offset hard box shadows (`shadow-[4px_4px_0px_0px_#000]`).
- **Typography:** Large, bold sans-serif with font weights `font-black` and `font-extrabold`.
- **Accent Badges:** Lime Green (`#84cc16`), Electric Blue (`#2563eb`), Amber Yellow (`#f59e0b`), Pink (`#ec4899`).
- **Header:** Compact navigation header featuring real-time clock, Persona Mode Dropdown (`Chief of Staff`, `Coach`, `Focus`, `Reflection`, `Planner`, `Reviewer`), Workspace Selector, and Navigation Tabs.
- **Voice Engine:** Speech-To-Text (Web Speech API) + Female Voice Synthesis (`pitch: 1.1`, filtering browser female voice registries).

---

## 🔌 API Endpoints Summary

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Server status & system version check |
| `/api/chat` | POST | Main conversational endpoint (processes intents, mutations, queries) |
| `/api/chat/history` | GET | Fetches past chat messages from SQLite |
| `/api/dashboard` | GET | Mission Control payload (briefing, analytics, goals, recent events) |
| `/api/goals` | GET / POST | List goals by workspace or create new living goal |
| `/api/goals/{id}` | DELETE | Delete goal by ID |
| `/api/timeline` | GET | Query Event Store with search & event_type filters |
| `/api/tasks` | GET / POST | List tasks or create new task |
| `/api/tasks/{id}/status` | PUT | Update task status (`COMPLETED`, `PENDING`) |
| `/api/knowledge` | GET / POST | Document storage & keyword search |
| `/api/reports` | GET | Dynamic AI reflection review (weekly/monthly) |
| `/api/analytics` | GET | Metrics (Consistency Score, Goal Velocity, Heatmap, Weight Trend) |
| `/api/memories` | GET | List stored memories by memory_type or category |
| `/api/workspaces` | GET | List all active workspaces |

---

## ⚡ How to Run Locally

### 1. Environment Setup
Create `backend/.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4o
DATABASE_URL=sqlite:///./lordsahu.db
```

### 2. Backend Server
```bash
cd backend
uv run uvicorn app.main:app --port 8000 --host 127.0.0.1
```

### 3. Frontend Dev Server
```bash
cd frontend
npm run dev -- --port 5173 --host
```

### 4. Run Pytest Suite
```bash
cd backend
uv run python -m pytest
```

---

## 🚀 Future Feature & Architectural Expansion Roadmap (For Other AI Tools & Engineers)

1. **Semantic Vector Search (RAG):** Integrate ChromaDB, FAISS, or Qdrant for dense embedding search over `memories` and `knowledge_docs`.
2. **Sub-Agent Swarm Orchestration:** Expand `core_orchestrator.py` into specialized sub-agents:
   - *Health & Fitness Agent* (analyzing weight trajectory, macro intake, sleep data).
   - *Academic & Learning Agent* (syllabus decomposition, flashcard generation, study interval scheduling).
   - *Financial & Expense Agent* (parsing receipts, tracking budgets).
3. **Real-time WebSockets / Streaming:** Stream LLM text tokens and voice audio chunks via WebSockets.
4. **Third-Party API Integrations:** Sync with Google Calendar, Notion, Apple HealthKit, and GitHub commits as automated background event producers into `EventEngine`.
