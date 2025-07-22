# 🧠 Health & Wellness Planner Agent

An AI-powered digital assistant built using the **OpenAI Agents SDK** and **Streamlit**, designed to help users achieve their **fitness**, **nutrition**, and **wellness goals**.

> Built with ❤️ by **S. M. Shan-e-Ali**

---

## 📌 Overview

This project is an intelligent multi-agent system that interacts naturally with users, understands their health-related goals, and offers customized support through smart tools and specialized agents.

It features real-time conversation streaming, session context tracking, and guardrails to ensure structured and meaningful responses.

---

## 🚀 Core Features

### 🔐 Secure Login  
- Users enter their name and workout level (Beginner / Intermediate / Advanced).  
- Personalized responses are generated accordingly.

### 💬 Chat Interface (via Streamlit)  
- GPT-style conversation window.
- User messages and assistant responses appear in chat bubbles.
- Real-time streamed replies using `runner.run_streamed()`.

### 🎯 Goal Analysis  
- Extracts structured goals (e.g., lose 5kg in 2 months) using a `GoalAnalyzerTool`.  
- Stores goals into session context using `UserSessionContext`.

### 🥗 Meal Planner  
- Generates a 7-day meal plan based on user's dietary preferences via `MealPlannerTool`.

### 🏋️ Workout Recommender  
- Creates workouts based on goal and experience level (`WorkoutRecommenderTool`).

### 🧠 Specialized Agent Handoffs  
- Delegates to expert sub-agents when needed:
  - `InjurySupportAgent` for pain/injury queries
  - `NutritionExpertAgent` for dietary advice
  - `EscalationAgent` for unsupported or urgent queries

### 🛡️ Guardrails  
- Input and output validation using:
  - `InputGuardrailTripwireTriggered`
  - `OutputGuardrailTripwireTriggered`

### 🧹 Chat Features  
- 🧾 **Clear History**: Removes all chat logs from session.
- 🔁 **Restore Mode**: Simulates ChatGPT's blank chat after clear.
- 🚪 **Logout**: Ends the session and returns to login screen.

---

## 📁 Project Structure

final_health_wellness/
│
├── agents/
│ ├── main_agent.py
│ ├── goal_analyzer_tool.py
│ ├── meal_planner_tool.py
│ ├── workout_recommender_tool.py
│ ├── scheduler_tool.py
│ ├── progress_tracker_tool.py
│ ├── injury_support_agent.py
│ ├── nutrition_expert_agent.py
│ └── escalation_agent.py
│
├── context/
│ └── user_session_context.py ← Pydantic model for session tracking
│
├── hooks/
│ └── my_hooks.py ← Implements on_tool_start, on_tool_end
│
├── guardrails/
│ ├── input_guardrail.py
│ └── output_guardrail.py
│
├── dashboard.py ← Streamlit UI
├── main.py ← Optional CLI runner
├── README.md
└── requirements.txt


---

## 🧰 Tech Stack

| Technology     | Purpose                                   |
|----------------|-------------------------------------------|
| **OpenAI Agents SDK** | Core agent system & streaming |
| **Streamlit**   | Web-based UI and chat interface          |
| **Pydantic**    | Schema validation for tools & context    |
| **Asyncio**     | Non-blocking streaming updates           |

---

## 📥 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/final_health_wellness.git
cd final_health_wellness

2. Create a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

3. Install Required Packages
pip install -r requirements.txt


🚦 Running the App
▶️ Streamlit Dashboard
streamlit run dashboard.py
python -m streamlit run dashboard.py

* Log in with your name and workout level

* Chat with the AI assistant

* Use Clear History or Logout as needed

🎯 Example Interaction
User: I want to lose 7kg in 3 months.

Assistant:
📊 Goal identified: Lose ~0.58kg/week

✅ Here's your 12-week plan:
- Calorie deficit: ~400/day
- Weekly workout split: HIIT, cardio, strength
- 7-day meal plan tailored to fat loss

👨‍💻 Author
S. M. Shan-e-Ali
Built this project with OpenAI Agents SDK + ❤️
Feel free to connect via GitHub or contribute to the repo!

