import json
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from app.models import DailyPlannerModel, PlannerItemModel, PlannerTemplateModel

class DailyPlannerRepository:
    """
    Daily Planner Repository Layer for LordSahu V1.4.
    Manages DailyPlannerModel, PlannerItemModel, and PlannerTemplateModel CRUD.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_today_planner(
        self,
        user_id: str = "default_user",
        day_boundary_time: str = "06:00"
    ) -> DailyPlannerModel:
        now = datetime.now(timezone.utc)
        boundary_hour = int(day_boundary_time.split(":")[0])
        
        # If current hour is before boundary, today belongs to previous calendar day
        if now.hour < boundary_hour:
            effective_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            effective_date = now.strftime("%Y-%m-%d")

        planner = self.db.query(DailyPlannerModel).filter(
            and_(
                DailyPlannerModel.user_id == user_id,
                DailyPlannerModel.date == effective_date
            )
        ).first()

        if not planner:
            # Archive older active planners
            self.db.query(DailyPlannerModel).filter(
                and_(
                    DailyPlannerModel.user_id == user_id,
                    DailyPlannerModel.status == "active",
                    DailyPlannerModel.date < effective_date
                )
            ).update({"status": "archived"})

            planner = DailyPlannerModel(
                user_id=user_id,
                date=effective_date,
                scope="daily",
                status="active",
                created_by="user",
                day_boundary_time=day_boundary_time
            )
            self.db.add(planner)
            self.db.commit()
            self.db.refresh(planner)

        return planner

    def add_item(
        self,
        planner_id: str,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        estimated_duration: Optional[str] = None,
        repeat_rule: Optional[str] = None,
        planner_source: str = "user",
        domains: List[str] = None
    ) -> PlannerItemModel:
        if not domains:
            domains = ["personal"]

        count = self.db.query(PlannerItemModel).filter(PlannerItemModel.planner_id == planner_id).count()

        item = PlannerItemModel(
            planner_id=planner_id,
            title=title,
            description=description,
            priority=priority,
            status="pending",
            start_time=start_time,
            end_time=end_time,
            estimated_duration=estimated_duration,
            repeat_rule=repeat_rule,
            planner_source=planner_source,
            domains=json.dumps(domains),
            related_life_entry_ids=json.dumps([]),
            order_index=count + 1
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_item(self, item_id: str, updates: Dict[str, Any]) -> Optional[PlannerItemModel]:
        item = self.db.query(PlannerItemModel).filter(PlannerItemModel.id == item_id).first()
        if not item:
            return None

        for k, v in updates.items():
            if k in ("domains", "related_life_entry_ids") and isinstance(v, list):
                setattr(item, k, json.dumps(v))
            elif hasattr(item, k):
                setattr(item, k, v)

        if updates.get("status") == "completed" and not item.completed_at:
            item.completed_at = datetime.now(timezone.utc)

        item.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(item)
        return item

    def complete_item(self, item_id: str, completion_source: str = "manual", life_entry_id: Optional[str] = None) -> Optional[PlannerItemModel]:
        item = self.db.query(PlannerItemModel).filter(PlannerItemModel.id == item_id).first()
        if not item:
            return None

        item.status = "completed"
        item.completion_source = completion_source
        item.completed_at = datetime.now(timezone.utc)

        if life_entry_id:
            try:
                ids = json.loads(item.related_life_entry_ids) if item.related_life_entry_ids else []
            except Exception:
                ids = []
            if life_entry_id not in ids:
                ids.append(life_entry_id)
                item.related_life_entry_ids = json.dumps(ids)

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_item(self, item_id: str) -> bool:
        item = self.db.query(PlannerItemModel).filter(PlannerItemModel.id == item_id).first()
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True

    def list_items(self, planner_id: str) -> List[PlannerItemModel]:
        return self.db.query(PlannerItemModel).filter(
            PlannerItemModel.planner_id == planner_id
        ).order_by(PlannerItemModel.order_index.asc()).all()

    def list_unfinished_from_yesterday(self, user_id: str = "default_user", today_date: str = "") -> List[PlannerItemModel]:
        yesterday_planner = self.db.query(DailyPlannerModel).filter(
            and_(
                DailyPlannerModel.user_id == user_id,
                DailyPlannerModel.date < today_date
            )
        ).order_by(desc(DailyPlannerModel.date)).first()

        if not yesterday_planner:
            return []

        return self.db.query(PlannerItemModel).filter(
            and_(
                PlannerItemModel.planner_id == yesterday_planner.id,
                PlannerItemModel.status.in_(["pending", "in_progress", "deferred"])
            )
        ).all()

    # Templates
    def create_template(self, user_id: str = "default_user", name: str = "Gym Day", items: List[Dict[str, Any]] = None) -> PlannerTemplateModel:
        template = PlannerTemplateModel(
            user_id=user_id,
            name=name,
            items_json=json.dumps(items or [])
        )
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def list_templates(self, user_id: str = "default_user") -> List[PlannerTemplateModel]:
        return self.db.query(PlannerTemplateModel).filter(PlannerTemplateModel.user_id == user_id).all()
