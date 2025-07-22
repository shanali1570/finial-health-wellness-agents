import asyncio
from context import UserSessionContext
from agent import main_agent
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from hooks import MyHooks

async def main():
    name = input("👤 What's your name? ").strip()

    experience = input("💪 What's your workout experience level? (beginner/intermediate/advanced): ").strip().lower()

    user_input = input(f"\n💬 Hello {name}! What's your health or fitness goal? \n👉 ")

    full_prompt = f"{user_input}\nMy workout experience level is: {experience}"

    context = UserSessionContext(name=name, uid=1)

    try:
        runner = Runner.run_streamed(
            starting_agent=main_agent,
            input=full_prompt,
            context=context,
            hooks=MyHooks(),
        )

        async for event in runner.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

        print("\n\n🧠 Final context state:")
        print(context.model_dump())

    except InputGuardrailTripwireTriggered as e:
        print("\n⚠️ Input validation failed:", e)
    except OutputGuardrailTripwireTriggered as e:
        print("\n⚠️ Output validation failed:", e)
    except Exception as e:
        print("\n❌ Unexpected error:", e)

if __name__ == "__main__":
    asyncio.run(main())
