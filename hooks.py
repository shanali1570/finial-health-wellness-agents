from agents import RunHooks, RunContextWrapper
from context import UserSessionContext
from agents import Agent, Tool


class MyHooks(RunHooks[UserSessionContext]):
    async def on_tool_start(
        self,
        context: RunContextWrapper[UserSessionContext],
        agent: Agent,
        tool: Tool,
    ):
        try:
            input_data = getattr(tool, "input", "N/A")
            print(f"🔧 Tool started: {tool.name} | Input: {input_data}")
        except Exception as e:
            print(f"🔧 Tool started: {tool.name} | Input logging failed: {e}")

    async def on_tool_end(
        self,
        context: RunContextWrapper[UserSessionContext],
        agent: Agent,
        tool: Tool,
        result: str,
    ):
        print(f"✅ Tool ended: {tool.name} | Result: {result}")

    async def on_handoff(
        self,
        context: RunContextWrapper[UserSessionContext],
        from_agent: Agent,
        to_agent: Agent,
    ):
        log_msg = f"🤝 Handoff from {from_agent.name} → {to_agent.name} (user: {context.context.name})"
        print(log_msg)
        context.context.handoff_logs.append(log_msg)
