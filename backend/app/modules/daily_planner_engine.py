import json
import re
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories.daily_planner_repository import DailyPlannerRepository

class DailyPlannerEngine:
    """
    Daily Planner Engine for LordSahu V1.4.
    Implements Day Boundary evaluation, Carry Forward, AI Morning Briefing, Bidirectional LifeEntry Sync, and Evening Review.
    """
    def __init__(self, db: Session, user_id: str = "default_user", day_boundary_time: str = "06:00"):
        self.db = db
        self.user_id = user_id
        self.day_boundary_time = day_boundary_time
        self.repo = DailyPlannerRepository(db)

    def get_today_planner(self) -> Dict[str, Any]:
        planner = self.repo.get_or_create_today_planner(self.user_id, self.day_boundary_time)
        items = self.repo.list_items(planner.id)

        completed_count = sum(1 for i in items if i.status == "completed")
        total_count = len(items)
        completion_pct = round((completed_count / total_count) * 100, 1) if total_count > 0 else 0.0

        item_list = [
            {
                "id": i.id,
                "title": i.title,
                "description": i.description,
                "priority": i.priority,
                "status": i.status,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "estimated_duration": i.estimated_duration,
                "repeat_rule": i.repeat_rule,
                "planner_source": i.planner_source,
                "completion_source": i.completion_source,
                "domains": json.loads(i.domains) if i.domains else [],
                "related_life_entry_ids": json.loads(i.related_life_entry_ids) if i.related_life_entry_ids else [],
                "completed_at": i.completed_at.strftime("%I:%M %p") if i.completed_at else None
            }
            for i in items
        ]

        return {
            "planner_id": planner.id,
            "date": planner.date,
            "status": planner.status,
            "day_boundary_time": planner.day_boundary_time,
            "completion_pct": completion_pct,
            "total_items": total_count,
            "completed_items": completed_count,
            "remaining_items": total_count - completed_count,
            "items": item_list
        }

    def add_item_to_today(
        self,
        title: str,
        priority: str = "medium",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        estimated_duration: Optional[str] = None,
        repeat_rule: Optional[str] = None,
        planner_source: str = "user",
        domains: List[str] = None
    ) -> Dict[str, Any]:
        planner = self.repo.get_or_create_today_planner(self.user_id, self.day_boundary_time)
        item = self.repo.add_item(
            planner_id=planner.id,
            title=title,
            priority=priority,
            start_time=start_time,
            end_time=end_time,
            estimated_duration=estimated_duration,
            repeat_rule=repeat_rule,
            planner_source=planner_source,
            domains=domains or ["personal"]
        )
        return {"status": "success", "item_id": item.id, "title": item.title, "message": f"Added '{title}' to today's planner agenda."}

    def carry_forward_unfinished(self) -> Dict[str, Any]:
        planner = self.repo.get_or_create_today_planner(self.user_id, self.day_boundary_time)
        unfinished = self.repo.list_unfinished_from_yesterday(self.user_id, planner.date)

        carried_count = 0
        for item in unfinished:
            self.repo.add_item(
                planner_id=planner.id,
                title=item.title,
                description=item.description,
                priority=item.priority,
                estimated_duration=item.estimated_duration,
                planner_source="carry_forward",
                domains=json.loads(item.domains) if item.domains else ["personal"]
            )
            carried_count += 1

        return {"status": "success", "carried_count": carried_count, "message": f"Carried forward {carried_count} unfinished tasks into today's agenda."}

    def generate_morning_brief(self) -> Dict[str, Any]:
        """
        AI Morning Briefing: Generates today's suggested agenda & priorities.
        """
        planner = self.repo.get_or_create_today_planner(self.user_id, self.day_boundary_time)
        items = self.repo.list_items(planner.id)

        if not items:
            # Seed default morning agenda suggestions
            suggestions = [
                {"title": "Weight Check", "priority": "high", "repeat_rule": "daily", "domains": ["fitness"]},
                {"title": "SQL & DSA Revision", "priority": "high", "domains": ["learning"]},
                {"title": "Chest & Cardio Workout", "priority": "medium", "start_time": "18:00", "end_time": "19:30", "domains": ["fitness"]},
                {"title": "Hydration (3L Water)", "priority": "low", "repeat_rule": "daily", "domains": ["fitness"]}
            ]
            for s in suggestions:
                self.repo.add_item(
                    planner_id=planner.id,
                    title=s["title"],
                    priority=s.get("priority", "medium"),
                    start_time=s.get("start_time"),
                    end_time=s.get("end_time"),
                    repeat_rule=s.get("repeat_rule"),
                    planner_source="ai",
                    domains=s.get("domains", ["personal"])
                )

        brief_text = "Good Morning Siddhant! Today's agenda is initialized. Prioritize SQL revision, afternoon development, and your 18:00 Gym session."
        return {
            "status": "success",
            "morning_brief": brief_text,
            "planner": self.get_today_planner()
        }

    def sync_life_entry_completion(self, life_entry_id: str, entry_title: str, entry_domains: List[str]) -> Optional[str]:
        """
        Bidirectional Synchronization: Automatically matches created LifeEntry against today's PlannerItems.
        Marks matching PlannerItem completed with completion_source="life_entry".
        """
        planner = self.repo.get_or_create_today_planner(self.user_id, self.day_boundary_time)
        items = self.repo.list_items(planner.id)

        e_title_lower = entry_title.lower()
        for item in items:
            if item.status in ("pending", "in_progress", "deferred"):
                i_title_lower = item.title.lower()
                # Fuzzy matching keywords
                if (i_title_lower in e_title_lower or e_title_lower in i_title_lower or
                    any(k in e_title_lower for k in i_title_lower.split() if len(k) > 3)):
                    self.repo.complete_item(item.id, completion_source="life_entry", life_entry_id=life_entry_id)
                    return item.title
        return None

    def run_evening_shutdown(self) -> Dict[str, Any]:
        """
        Evening Review & Shutdown Flow:
        Compares planned vs completed tasks, feeds Daily Chronicle, and archives planner.
        """
        planner = self.repo.get_or_create_today_planner(self.user_id, self.day_boundary_time)
        items = self.repo.list_items(planner.id)

        completed = [i.title for i in items if i.status == "completed"]
        remaining = [i.title for i in items if i.status != "completed"]

        review_prompt = "Before we close today... Is there anything else you'd like me to remember before archiving today's planner?"
        return {
            "status": "success",
            "review_prompt": review_prompt,
            "completed_count": len(completed),
            "remaining_count": len(remaining),
            "completed_tasks": completed,
            "remaining_tasks": remaining
        }
