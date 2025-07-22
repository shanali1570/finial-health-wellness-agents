import streamlit as st
import asyncio
from datetime import datetime
from agents import Runner
from agent import main_agent
from context import UserSessionContext
from hooks import MyHooks
from openai.types.responses import ResponseTextDeltaEvent
from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered

# Set page config
st.set_page_config(page_title="Health & Wellness Planner", layout="centered")

# Session state setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "context" not in st.session_state:
    st.session_state.context = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "trigger_clear" not in st.session_state:
    st.session_state.trigger_clear = False
if "experience" not in st.session_state:
    st.session_state.experience = ""
if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False

# Handle clear history
if st.session_state.trigger_clear:
    st.session_state.chat_history = []
    st.session_state.trigger_clear = False
    st.rerun()

# Sidebar menu
with st.sidebar:
    st.title("☰ Menu")

    if st.session_state.logged_in:
        st.markdown(f"👋 Hello, **{st.session_state.context.name}**")

        if st.button("🚪 Logout", key="logout_button"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.logged_in = False
            st.rerun()

        # Clear history button
        st.button("🧹 Clear History", on_click=lambda: st.session_state.__setitem__("trigger_clear", True))

    st.markdown("---")
    st.markdown("Built with ❤️ by **S. M. Shan-e-Ali** using OpenAI Agents SDK")


# Greeting helper
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "🌅 Good morning"
    elif 12 <= hour < 17:
        return "🌞 Good afternoon"
    elif 17 <= hour < 21:
        return "🌇 Good evening"
    else:
        return "🌙 Good night"

# Login page
if not st.session_state.logged_in:
    st.title("🔐 Welcome to Wellness Planner")

    with st.form("login_form"):
        name = st.text_input("👤 Enter your name")
        experience = st.selectbox("💪 Your workout level", ["Beginner", "Intermediate", "Advanced"])
        submitted = st.form_submit_button("Login")

        if submitted and name.strip():
            st.session_state.logged_in = True
            st.session_state.context = UserSessionContext(name=name.strip(), uid=1)
            st.session_state.experience = experience.lower()
            st.rerun()

    st.markdown("---")
    st.markdown("Built with ❤️ by **S. M. Shan-e-Ali** using OpenAI Agents SDK")

# Main assistant interface
else:
    greeting = get_greeting()
    st.title(f"{greeting}, {st.session_state.context.name}! 👋")
    st.markdown("Ask me anything about your health goals, fitness, or nutrition. I'm here to help!")

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])

    # Handle user input
    user_input = st.chat_input("How can I help you today?")
    if user_input:
        full_prompt = f"{user_input}\nMy workout experience level is: {st.session_state.experience}"
        st.session_state.chat_history.append({"role": "user", "text": user_input})

        with st.chat_message("assistant"):
            response_box = st.empty()

            async def run_agent():
                try:
                    runner = Runner.run_streamed(
                        starting_agent=main_agent,
                        input=full_prompt,
                        context=st.session_state.context,
                        hooks=MyHooks(),
                    )

                    full_response = ""
                    async for event in runner.stream_events():
                        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                            full_response += event.data.delta
                            response_box.markdown(full_response + "▌")

                    response_box.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "text": full_response})

                except InputGuardrailTripwireTriggered as e:
                    response_box.error(f"⚠️ Input validation failed: {e}")
                except OutputGuardrailTripwireTriggered as e:
                    response_box.error(f"⚠️ Output validation failed: {e}")
                except Exception as e:
                    response_box.error(f"❌ Error: {str(e)}")

            asyncio.run(run_agent())
