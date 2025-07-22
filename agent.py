from agents import Agent, handoff
from agents_folder.nutrition_expert_agent import NutritionExpertAgentFactory, log_nutrition_handoff
from agents_folder.injury_support_agent import InjurySupportAgentFactory, log_injury_handoff
from agents_folder.escalation_agent import EscalationAgentFactory, log_escalation
from tools.goal_analyzer import analyze_goal
from tools.user_info_tool import process_user_tool
from tools.meal_planner import suggest_meal_plan
from tools.workout_recommender import recommend_workout
from tools.checkin_scheduler import schedule_checkins
from tools.progress_tracker import track_progress
from guardrails.input_guardrails import goal_input_guardrail
from guardrails.output_guardrails import tool_output_guardrail
from dotenv import load_dotenv
load_dotenv()


NutritionExpertAgent = NutritionExpertAgentFactory()
InjurySupportAgent = InjurySupportAgentFactory()
EscalationAgent = EscalationAgentFactory()


main_agent = Agent(
    name="Main Health Agent",
    
    instructions="""
            You are a wellness coach.Assist user with fitness goals using tools. Understand and store user's health goal, or process user info and offer meal planning if needed.
    
            🎯 Responsibilities:
            - Extract user fitness goals (e.g., 'lose 5kg in 2 months') via `analyze_goal` tool.
            - Hand off to sub-agents based on user needs:
            - nutrition → NutritionExpertAgent
            - injury/pain → InjurySupportAgent
            - human coach → EscalationAgent

            🧠 Always call `analyze_goal` when a user gives a goal involving quantity + duration.
            🤝 Multi-goal handling:
            - Extract goal via `analyze_goal`
            - Then hand off based on condition
            - Never manually parse the input

                """,
    
    tools=[
        analyze_goal, 
        process_user_tool, 
        suggest_meal_plan, 
        recommend_workout, 
        schedule_checkins, 
        track_progress],

     handoffs=[
        handoff(
            agent=NutritionExpertAgent,
            on_handoff=log_nutrition_handoff,
            tool_name_override="nutrition_assistance",
            tool_description_override="Handles dietary, diabetic, and allergy-related questions."
        ),
        handoff(
            agent=InjurySupportAgent,
            on_handoff=log_injury_handoff,
            tool_name_override="injury_support",
            tool_description_override="Connects user to injury support assistant for physical pain or injury guidance."
        ),
        handoff(
            agent=EscalationAgent,
            on_handoff=log_escalation,
            tool_name_override="connect_to_human_trainer",
            tool_description_override="Connects the user to a human trainer for personalized coaching."
        )
    ],
    
    input_guardrails=[goal_input_guardrail],
    
    output_guardrails=[tool_output_guardrail],
    
    model="gpt-4.1-mini", 
)
