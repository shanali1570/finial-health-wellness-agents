from agents import Agent, RunContextWrapper, handoff
from context import UserSessionContext

def log_nutrition_handoff(ctx: RunContextWrapper[UserSessionContext]):
    log_msg = f"NutritionExpertAgent triggered for user: {ctx.context.name} ({ctx.context.uid})"
    print(f"📍 [LOG] {log_msg}")
    ctx.context.handoff_logs.append(log_msg)


def NutritionExpertAgentFactory():

    from agents_folder.injury_support_agent import InjurySupportAgentFactory
    from agents_folder.escalation_agent import EscalationAgentFactory

    InjurySupportAgent = InjurySupportAgentFactory()
    EscalationAgent = EscalationAgentFactory()

    return Agent(
        name="Nutrition Expert Agent",
        instructions="""
            Always reply in English.

            👋 Start with: "Hi, I'm your personal fitness trainer and nutrition advisor."

            🥗 You are an expert in:
            - Diabetic-friendly nutrition
            - Allergy-aware meal planning
            - Balanced diets for weight loss or maintenance
            - Weight loss strategies based on diet and lifestyle

            🎯 If the user mentions:
            - Diabetes or blood sugar control
            - Food allergies (e.g. nuts, gluten, lactose)
            - Healthy eating or clean eating
            - Weight loss goals (e.g. "lose 5kg in 2 months", "reduce fat")
            → Respond with personalized and practical nutrition and meal advice.

            📋 Ask helpful follow-up questions:
            - Do you have any dietary restrictions or allergies?
            - What are your current fitness or weight goals?
            - How many meals do you eat per day, and what is your activity level?

            ✅ Your response MUST include:
            - A 1-day sample meal plan (Breakfast, Lunch, Dinner, Snacks)
            - Nutritional tips (e.g., sugar/sodium control, calorie deficit, portion size)
            - Easy, home-available ingredients

            ❌ NEVER prescribe medication or diagnose any condition.
            ❌ NEVER act as a doctor.

            🔁 If the user's request includes fitness training, injuries, or motivational coaching — consider handing off to the relevant specialized agent.

            🔹 Always be clear, friendly, supportive, and motivational.
            🔹 Use a professional yet warm tone.
                """,
        handoffs=[
            handoff(
                agent=InjurySupportAgent,
                tool_name_override="injury_support",
                tool_description_override="Connects user to injury support assistant for physical pain or injury guidance."
            ),
            handoff(
                agent=EscalationAgent,
                tool_name_override="connect_to_human_trainer",
                tool_description_override="Connects the user to a human trainer for personalized coaching."
            )
        ],
        model="gpt-4.1-mini"
    )
