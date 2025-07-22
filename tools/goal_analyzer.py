from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from pydantic import BaseModel
import re

class AnalyzeGoalArgs(BaseModel):
    user_input: str

@function_tool
async def analyze_goal(ctx: RunContextWrapper[UserSessionContext], args: AnalyzeGoalArgs) -> dict:
    print(f"\n🔍 User said: {args.user_input}\n")

    match = re.search(
        r'(?:lose|reduce|cut|drop)\s+(\d+(?:\.\d+)?)\s*(?:kg|kilograms)?(?:\s*(?:in|within|over))?\s*(\d+)\s*(days?|weeks?|months?)',
        args.user_input.lower()
    )

    if match:
        amount = float(match.group(1))
        duration_value = int(match.group(2))
        duration_unit = match.group(3)
        duration = f"{duration_value} {duration_unit}"

        extracted_goal = {
            "goal_type": "lose_weight",
            "amount": amount,
            "unit": "kg",
            "duration": duration,
            "raw_goal": args.user_input,
        }
        ctx.context.goal = extracted_goal
        print("✅ Stored in context:", ctx.context.model_dump())

        return {
            "result": f"Great! You've set a goal to lose {amount}kg in {duration}. Let's build a personalized plan for that!"
        }

    fallback_goal = {
        "goal_type": "unknown",
        "amount": None,
        "unit": None,
        "duration": None,
        "raw_goal": args.user_input
    }
    ctx.context.goal = fallback_goal
    print("⚠️ Stored fallback goal in context:", ctx.context.model_dump())

    return {
        "result": "I couldn't quite understand your goal. Could you rephrase it like: 'I want to lose 5kg in 2 months'?"
    }
