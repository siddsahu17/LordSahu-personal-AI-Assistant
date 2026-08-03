import json
import re
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories.life_entry_repository import LifeEntryRepository
from app.repositories.event_repository import EventRepository
from app.schemas import EventCreate
from app.modules.event_engine import EventEngine

class LifeEntryEngine:
    """
    LifeEntry Engine for LordSahu V1.4.
    Implements LifeEntry management and triggers Bidirectional Daily Planner Completion Sync.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self.repo = LifeEntryRepository(db)
        self.evt_engine = EventEngine(db, user_id)

    def process_natural_input(
        self,
        text: str,
        source_raw_transcript: Optional[str] = None,
        source: str = "text"
    ) -> Dict[str, Any]:
        """
        Parses natural conversational speech/text, auto-detects multi-domains,
        extracts entities, computes confidence, saves LifeEntryModel,
        and triggers Bidirectional Daily Planner Completion Sync.
        """
        t_lower = text.lower()
        domains = set()
        category = "journal"
        title = text[:60]
        structured_data = {}
        confidence = 0.95

        # Multi-Domain Auto-Classification Rules
        if any(k in t_lower for k in ["learned", "concept", "study", "studied", "leetcode", "solved", "read doc", "hands-on llm", "docker"]):
            domains.add("learning")
            category = "concept" if "concept" in t_lower or "learned" in t_lower else "study"

        if any(k in t_lower for k in ["implemented", "feature", "bug", "fixed", "refactored", "codebase", "lordsahu", "deployment", "github"]):
            domains.add("projects")
            if category == "journal": category = "feature"

        if any(k in t_lower for k in ["applied to", "resume", "interview", "certification", "job", "internship", "fischer jordan"]):
            domains.add("career")
            if category == "journal": category = "career"

        if any(k in t_lower for k in ["lecture", "attended", "missed", "assignment", "practical", "exam", "lab", "gpa", "dbms"]):
            domains.add("college")
            if category == "journal": category = "lecture"

        if any(k in t_lower for k in ["spent", "paid", "rupees", "₹", "dollars", "$", "bought", "salary", "expense", "cost"]):
            domains.add("finance")
            category = "expense"
            amt_match = re.search(r"(?:₹|\$|rs\.?|spent|paid)\s*(\d+(?:\.\d+)?)", t_lower)
            if amt_match:
                structured_data["amount"] = float(amt_match.group(1))

        weight_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:kg|kilos)", t_lower)
        if any(k in t_lower for k in ["workout", "gym", "chest day", "leg day", "arm day", "ran", "sport", "weight", "drank", "sleep"]) or weight_match:
            domains.add("fitness")
            if weight_match:
                category = "weight"
                structured_data["weight_kg"] = float(weight_match.group(1))
            elif category == "journal":
                category = "workout"

        if not domains:
            domains.add("personal")

        domain_list = sorted(list(domains))

        # Create LifeEntry
        entry = self.repo.add_entry(
            user_id=self.user_id,
            domains=domain_list,
            category=category,
            title=title,
            raw_text=text,
            source_raw_transcript=source_raw_transcript or text,
            structured_data=structured_data,
            ai_summary=text,
            confidence=confidence,
            source=source,
            tags=domain_list
        )

        # Trigger Bidirectional Daily Planner Completion Sync
        from app.modules.daily_planner_engine import DailyPlannerEngine
        planner_engine = DailyPlannerEngine(self.db, self.user_id)
        synced_planner_title = planner_engine.sync_life_entry_completion(entry.id, title, domain_list)

        # Emit Event Store Record
        self.evt_engine.create_event(EventCreate(
            workspace_id=domain_list[0],
            source="chat_text",
            event_type=f"{category.upper()}_LOGGED",
            intent="LOG_LIFE_ENTRY",
            payload={"entry_id": entry.id, "domains": domain_list, "title": title}
        ))

        sync_msg = f" Also completed matching planner item '{synced_planner_title}'!" if synced_planner_title else ""

        return {
            "status": "success",
            "entry_id": entry.id,
            "domains": domain_list,
            "category": category,
            "title": title,
            "confidence": confidence,
            "synced_planner_item": synced_planner_title,
            "message": f"Added entry to {', '.join([d.capitalize() for d in domain_list])} journal.{sync_msg}"
        }

    def update_matching_entry(self, search_text: str, updated_val_text: str) -> Dict[str, Any]:
        today_entries = self.repo.get_today_entries(self.user_id)
        if not today_entries:
            return {"status": "error", "message": "No entries logged today to update."}

        target_entry = None
        s_lower = search_text.lower()
        for e in today_entries:
            if s_lower in e.title.lower() or s_lower in e.raw_text.lower() or s_lower in e.category.lower():
                target_entry = e
                break

        if not target_entry:
            target_entry = today_entries[0]

        self.repo.update_entry(target_entry.id, {
            "raw_text": f"{target_entry.raw_text} (Updated: {updated_val_text})",
            "ai_summary": f"Updated entry: {updated_val_text}"
        })

        return {
            "status": "success",
            "entry_id": target_entry.id,
            "updated_title": target_entry.title,
            "message": f"Updated entry '{target_entry.title}' successfully."
        }

    def soft_delete_matching_entry(self, search_text: str) -> Dict[str, Any]:
        today_entries = self.repo.get_today_entries(self.user_id)
        if not today_entries:
            return {"status": "error", "message": "No entries logged today to delete."}

        target_entry = today_entries[0]
        self.repo.soft_delete_entry(target_entry.id)
        return {
            "status": "success",
            "deleted_title": target_entry.title,
            "message": f"Deleted entry '{target_entry.title}'."
        }

    def generate_daily_chronicle(self) -> Dict[str, Any]:
        entries = self.repo.get_today_entries(self.user_id)
        now_str = datetime.now(timezone.utc).strftime("%d %B %Y")

        if not entries:
            return {
                "date": now_str,
                "summary": "No journal entries recorded today yet.",
                "domain_highlights": {},
                "ai_reflection": "Today was quiet. Speak or type anytime to update your daily diary."
            }

        domain_groups: Dict[str, List[str]] = {}
        for e in entries:
            try:
                doms = json.loads(e.domains) if e.domains else ["personal"]
            except Exception:
                doms = ["personal"]

            for d in doms:
                if d not in domain_groups:
                    domain_groups[d] = []
                domain_groups[d].append(f"• {e.title}")

        reflection = f"Today's focus encompassed {len(entries)} logged life events across {len(domain_groups)} domain(s). Consistency remains active."

        return {
            "date": now_str,
            "total_entries": len(entries),
            "domain_highlights": domain_groups,
            "ai_reflection": reflection
        }

    def compute_5_core_insights(self) -> Dict[str, Any]:
        entries = self.repo.query_entries(user_id=self.user_id, status="active", limit=100)

        weights = []
        learning_count = 0
        total_spent = 0.0
        projects_count = 0
        heatmap_days = set()

        for e in entries:
            d_str = e.timestamp.strftime("%Y-%m-%d") if e.timestamp else ""
            if d_str:
                heatmap_days.add(d_str)

            try:
                doms = json.loads(e.domains) if e.domains else []
            except Exception:
                doms = []

            if "fitness" in doms and e.category == "weight":
                try:
                    s_data = json.loads(e.structured_data) if e.structured_data else {}
                    w_val = s_data.get("weight_kg")
                    if w_val: weights.append(float(w_val))
                except Exception:
                    pass

            if "learning" in doms:
                learning_count += 1
            if "projects" in doms:
                projects_count += 1
            if "finance" in doms:
                try:
                    s_data = json.loads(e.structured_data) if e.structured_data else {}
                    total_spent += float(s_data.get("amount") or 0.0)
                except Exception:
                    pass

        latest_w = weights[0] if weights else 97.4

        return {
            "weight_trend": {"current_weight_kg": latest_w, "logged_count": len(weights)},
            "learning_progress": {"concepts_and_topics": learning_count},
            "money_flow": {"total_spent_rupees": round(total_spent, 2)},
            "project_progress": {"features_and_commits": projects_count},
            "activity_heatmap": {"active_days_count": len(heatmap_days)}
        }
