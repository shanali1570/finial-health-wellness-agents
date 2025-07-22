from typing import Any
from pydantic import BaseModel
from agents import RunContextWrapper, FunctionTool
from pydantic import BaseModel

class FunctionArgs(BaseModel):
    username: str
    age: int


def do_some_work(data: str) -> str:
    return f"✅ {data} processed."

async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")

schema = FunctionArgs.model_json_schema()
schema["additionalProperties"] = False

process_user_tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=schema,
    on_invoke_tool=run_function,
)
