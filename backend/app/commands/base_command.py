from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

class BaseCommand:
    """
    Base Command encapsulating discrete business operations.
    Supports execute() and compensation rollback().
    """
    def __init__(self, db: Session, user_id: str = "default_user"):
        self.db = db
        self.user_id = user_id

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def rollback(self, params: Dict[str, Any]) -> None:
        pass
