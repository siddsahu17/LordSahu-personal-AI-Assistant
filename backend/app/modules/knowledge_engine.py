import json
import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import KnowledgeDocModel
from app.schemas import KnowledgeDocCreate

DEFAULT_KNOWLEDGE = [
    {
        "title": "DBMS Semester 5 Syllabus & Exam Schedule",
        "workspace_id": "learning",
        "doc_type": "syllabus",
        "content": "Course covers Relational Algebra, SQL Joins, Indexing, Transactions, Normalization 1NF to BCNF, and ER Diagrams. Final Exam in December."
    },
    {
        "title": "Hypertrophy Workout & Fitness Blueprint",
        "workspace_id": "fitness",
        "doc_type": "workout_plan",
        "content": "Push/Pull/Legs 4-day split. Target 10,000 steps daily. Target weight 80kg with calorie deficit of 500 kcal/day."
    }
]

class KnowledgeEngine:
    """
    Knowledge Engine manages document storage (PDFs, resumes, syllabi) and semantic knowledge retrieval.
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id
        self._ensure_defaults()

    def _ensure_defaults(self):
        count = self.db.query(KnowledgeDocModel).filter(KnowledgeDocModel.user_id == self.user_id).count()
        if count == 0:
            for doc in DEFAULT_KNOWLEDGE:
                db_doc = KnowledgeDocModel(
                    id=str(uuid.uuid4()),
                    user_id=self.user_id,
                    workspace_id=doc["workspace_id"],
                    title=doc["title"],
                    doc_type=doc["doc_type"],
                    content=doc["content"]
                )
                self.db.add(db_doc)
            self.db.commit()

    def add_document(self, doc_data: KnowledgeDocCreate) -> KnowledgeDocModel:
        db_doc = KnowledgeDocModel(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            workspace_id=doc_data.workspace_id,
            title=doc_data.title,
            doc_type=doc_data.doc_type,
            content=doc_data.content,
            metadata_json=json.dumps(doc_data.metadata_json)
        )
        self.db.add(db_doc)
        self.db.commit()
        self.db.refresh(db_doc)
        return db_doc

    def list_documents(self, workspace_id: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.db.query(KnowledgeDocModel).filter(KnowledgeDocModel.user_id == self.user_id)
        if workspace_id and workspace_id != "all":
            query = query.filter(KnowledgeDocModel.workspace_id == workspace_id)
        docs = query.order_by(KnowledgeDocModel.created_at.desc()).all()

        return [
            {
                "id": d.id,
                "title": d.title,
                "workspace_id": d.workspace_id,
                "doc_type": d.doc_type,
                "content_preview": d.content[:150] + "..." if len(d.content) > 150 else d.content,
                "created_at": d.created_at.isoformat() if d.created_at else None
            }
            for d in docs
        ]

    def search_knowledge(self, query_text: str) -> List[str]:
        words = set(query_text.lower().split())
        docs = self.db.query(KnowledgeDocModel).filter(KnowledgeDocModel.user_id == self.user_id).all()
        matches = []
        for d in docs:
            doc_words = set(d.content.lower().split())
            if words.intersection(doc_words):
                matches.append(f"[{d.title}]: {d.content[:200]}")
        return matches
