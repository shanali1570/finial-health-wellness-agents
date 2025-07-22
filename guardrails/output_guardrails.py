from pydantic import BaseModel
from typing import List
from agents import Agent, GuardrailFunctionOutput, output_guardrail, Runner, RunContextWrapper


class ToolOutputCheck(BaseModel):
    valid: bool
    error_fields: List[str] = []


# Agent to validate tool output
# ✅ Simpler output guardrail - just ensure output is not empty or obviously broken
check_agent = Agent(
    name="Tool Output Guardrail",
    instructions="""
        You are validating output from a tool.

        - If the output is a dictionary with keys like 'level' and 'exercises', make sure:
        - 'level' is a non-empty string
        - 'exercises' is a non-empty list of strings

        - If the output is plain text or Markdown, just mark it as valid if it's informative and non-empty.

        Return:
        - valid: true if acceptable
        - valid: false if it's empty, gibberish, or structurally invalid
        - error_fields: describe what’s wrong
        """,
    model="gpt-4.1-mini",
    output_type=ToolOutputCheck,
)


@output_guardrail
async def tool_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: dict):
    result = await Runner.run(check_agent, output, context=ctx.context)
    check = result.final_output_as(ToolOutputCheck)
    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=not check.valid
    )
