from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.database import Base

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    """
    Generic Base Repository providing decoupled database operations.
    """
    def __init__(self, db: Session, model_cls: Type[T]):
        self.db = db
        self.model_cls = model_cls

    def get_by_id(self, entity_id: str) -> Optional[T]:
        return self.db.query(self.model_cls).filter(self.model_cls.id == entity_id).first()

    def add(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        self.db.delete(entity)
        self.db.commit()
