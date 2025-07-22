from pydantic import BaseModel
from typing import Optional, List, Dict

class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[dict] = None
    meal_plan: Optional[List[str]] = None
    workout_plan: Optional[dict] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = []  
