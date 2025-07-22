from agents import function_tool, RunContextWrapper
from pydantic import BaseModel
from typing import List
from context import UserSessionContext

class MealPlannerArgs(BaseModel):
    dietary_preference: str  

@function_tool
async def suggest_meal_plan(ctx: RunContextWrapper[UserSessionContext], args: MealPlannerArgs) -> str:
    preference = args.dietary_preference.lower()
    
    sample_meals = {
        "vegetarian": [
            "Day 1: Chickpea salad + quinoa",
            "Day 2: Lentil soup + whole grain toast",
            "Day 3: Veggie stir-fry with tofu",
            "Day 4: Greek salad + baked sweet potato",
            "Day 5: Vegetable curry + brown rice",
            "Day 6: Pasta primavera",
            "Day 7: Oatmeal + berries + nuts"
        ],
        "keto": [
            "Day 1: Scrambled eggs + avocado",
            "Day 2: Grilled chicken + zucchini noodles",
            "Day 3: Steak + cauliflower mash",
            "Day 4: Tuna salad lettuce wraps",
            "Day 5: Eggs + spinach + mushrooms",
            "Day 6: Salmon + asparagus",
            "Day 7: Zucchini boats with ground beef"
        ],
        "balanced": [
            "Day 1: Grilled chicken + veggies + brown rice",
            "Day 2: Oatmeal + banana + almond butter",
            "Day 3: Turkey wrap + fruit salad",
            "Day 4: Salmon + quinoa + spinach",
            "Day 5: Bean burrito bowl",
            "Day 6: Egg sandwich + smoothie",
            "Day 7: Baked chicken + sweet potato + broccoli"
        ]
    }

    meals = sample_meals.get(preference, sample_meals["balanced"])
    ctx.context.meal_plan = meals

    return (
        f"✅ 7-day meal plan for a **{preference}** diet:\n\n" +
        "\n".join(meals)
    )
