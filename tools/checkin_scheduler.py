from typing import Literal
from pydantic import BaseModel
from agents import function_tool, RunContextWrapper
from context import UserSessionContext


class CheckinInput(BaseModel):
    frequency: Literal["daily", "weekly", "monthly"] = "weekly"


@function_tool
async def schedule_checkins(ctx: RunContextWrapper[UserSessionContext], args: CheckinInput) -> str:
    note = f"📝 Scheduled {args.frequency} check-ins."

    ctx.context.progress_logs.append({
        "frequency": args.frequency,
        "status": "scheduled"
    })

    return note
