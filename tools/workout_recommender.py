from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from pydantic import BaseModel

class WorkoutInput(BaseModel):
    experience_level: str

@function_tool
async def recommend_workout(ctx: RunContextWrapper[UserSessionContext], args: WorkoutInput) -> dict:
    experience = args.experience_level.lower()

    beginner_plan = [
        "30 min Brisk Walk - Daily",
        "Bodyweight Squats - 2 sets of 12 reps, 3 times a week",
        "Knee Push-ups - 2 sets of 10 reps, 3 times a week",
        "Plank - Hold for 30 seconds, 3 times a week"
    ]

    intermediate_plan = [
        "45 min Jogging - 4x a week",
        "Lunges - 3 sets of 15 reps",
        "Push-ups - 3 sets of 15 reps",
        "Plank - Hold for 1 min"
    ]

    advanced_plan = [
        "60 min HIIT - 5x a week",
        "Weighted Squats - 4 sets of 10 reps",
        "Pull-ups - 4 sets of 8 reps",
        "Plank - Hold for 2 min"
    ]

    plans = {
        "beginner": beginner_plan,
        "intermediate": intermediate_plan,
        "advanced": advanced_plan
    }

    selected_plan = plans.get(experience, beginner_plan)

    ctx.context.workout_plan = {
        "level": experience,
        "exercises": selected_plan
    }

    return {
        "level": experience,
        "exercises": selected_plan
    }
