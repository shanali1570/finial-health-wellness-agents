from datetime import datetime
from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from pydantic import BaseModel
from typing import Optional

class ProgressInput(BaseModel):
    date: Optional[str] = None  
    weight: Optional[float] = None  
    mood: Optional[str] = None
    note: Optional[str] = None
    
@function_tool
async def track_progress(ctx: RunContextWrapper[UserSessionContext], args: ProgressInput) -> str:
    log_entry = {
        "date": args.date or datetime.today().strftime("%Y-%m-%d"),
        "weight": f"{args.weight} kg" if args.weight else None,
        "mood": args.mood,
        "note": args.note,
    }

    log_entry = {k: v for k, v in log_entry.items() if v is not None}
    ctx.context.progress_logs.append(log_entry)

    return f"📈 Progress recorded for {log_entry['date']}."
