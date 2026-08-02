from typing import Callable, Dict, List, Any

class EventBus:
    """
    Lightweight, decoupled, internal Event Bus abstraction for LordSahu AI OS.
    Handles pub/sub event distribution across subscribers (GoalProgress, Analytics, MemoryAging).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance.subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        return cls._instance

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        if handler not in self.subscribers[event_type]:
            self.subscribers[event_type].append(handler)

    def publish(self, event_type: str, event_data: Dict[str, Any]) -> None:
        # Generic wildcard subscribers
        all_handlers = self.subscribers.get("*", []) + self.subscribers.get(event_type, [])
        for handler in all_handlers:
            try:
                handler(event_data)
            except Exception as e:
                print(f"[EventBus Subscriber Warning]: Failed executing handler for '{event_type}': {e}")

# Global EventBus Singleton
event_bus = EventBus()
