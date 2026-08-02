from datetime import datetime, timezone
from typing import Dict, Any

class OSStateEngine:
    """
    OS Phase State Engine tracking the operator's daily cycle (JARVIS-like phase awareness).
    Phases: MORNING_BRIEFING, DEEP_WORK, MIDDAY_BREAK, EVENING_FITNESS, NIGHT_REFLECTION, SLEEP.
    """
    def get_current_phase(self, dt: datetime = None) -> Dict[str, Any]:
        if dt is None:
            dt = datetime.now()

        hour = dt.hour

        if 5 <= hour < 9:
            phase = "MORNING_BRIEFING"
            label = "Morning Briefing & Alignment"
            focus = "Review goals, check top priority, set daily intention."
        elif 9 <= hour < 13:
            phase = "DEEP_WORK"
            label = "Deep Work Session (Morning)"
            focus = "High focus, distraction-free execution."
        elif 13 <= hour < 14:
            phase = "MIDDAY_BREAK"
            label = "Midday Meal & Reset"
            focus = "Rest, recharge, review morning progress."
        elif 14 <= hour < 18:
            phase = "DEEP_WORK"
            label = "Deep Work Session (Afternoon)"
            focus = "Task completion, learning assignments, build tasks."
        elif 18 <= hour < 20.5:
            phase = "EVENING_FITNESS"
            label = "Evening Fitness & Movement"
            focus = "Workouts, cardio, physical health check-in."
        elif 20.5 <= hour < 23:
            phase = "NIGHT_REFLECTION"
            label = "Night Reflection & Review"
            focus = "Log evening study, review day's events, prepare for sleep."
        else:
            phase = "SLEEP"
            label = "Sleep & Recovery"
            focus = "Restoration, mental recovery."

        return {
            "phase": phase,
            "label": label,
            "focus": focus,
            "current_hour": hour,
            "formatted_time": dt.strftime("%I:%M %p")
        }
