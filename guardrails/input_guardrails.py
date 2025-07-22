from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    input_guardrail,
    Runner,
    RunContextWrapper,
    TResponseInputItem,
)
from typing import Union

class GoalCheckOutput(BaseModel):
    valid: bool
    reason: str

guardrail_agent = Agent(
    name="Goal Format Guardrail",
    instructions="""
        Check if the user input is a valid health-related request or context. Accept if it is:

        - A fitness goal (e.g. 'lose 5kg in 2 months', 'gain muscle')
        - A diet or meal plan request (e.g. 'Give me a keto meal plan', 'I'm vegetarian')
        - A workout or exercise question (e.g. 'suggest workouts', 'I need a plan')
        - A health condition or context (e.g. 'I am diabetic', 'I have a knee injury')
        - A progress tracking update (e.g. 'Today I weighed 70kg', 'I ran 5km')

        Return valid=True if the message helps the assistant provide relevant health or fitness advice.
        Otherwise, return valid=False with a short reason.
    """,
    model="gpt-4.1-mini",
    output_type=GoalCheckOutput,
)

@input_guardrail
async def goal_input_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    user_input: Union[str, list[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    # Extract plain text from input
    if isinstance(user_input, str):
        text = user_input
    elif isinstance(user_input, list) and user_input:
        text = user_input[-1].get("content", "")
    else:
        text = ""

    # Run the guardrail agent to validate the message
    result = await Runner.run(guardrail_agent, text, context=ctx.context)
    check = result.final_output_as(GoalCheckOutput)

    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=not check.valid
    )
