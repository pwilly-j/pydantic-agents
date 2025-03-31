#import libraries, you will need a requirements file for this
import nest_asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel, Field

nest_asyncio.apply()

#Define the model you would like to use
model = OpenAIModel("gpt-4o")

#Define basic agent parameters
basic_agent = Agent(
    model=model,
    system_prompt="You are a helpful customer support agent. Be concise and friendly."
)

basic_response = basic_agent.run_sync("How can I track my order #12345")
#print(dir(basic_response))
print(basic_response.data)
print(basic_response.all_messages())
print(basic_response.cost())

#------------------------------------------------
# Agent with a structured response
#------------------------------------------------
"""
This example shows how to get structured, type safe responses from the agent.
- Use Pydantic modesl to define the response structure
- Type validation and safety
- Field descriptions for better model understanding
"""

class ResponseModel(BaseModel):
    """Structured response with metadata"""

    structured_response: str 
    needs_escalation: bool
    follow_up_required: bool
    sentiments: str = Field(description="Customer sentiment analysis")

structured_agent = Agent(
    model=model,
    result_type=ResponseModel,
    system_prompt=(
        "You are an intelligent customer support agent."
        "Analyze queries carefully and provide a structured response"
    ),
)

structured_response = structured_agent.run_sync("How can I track my order #12345")
print(structured_response.data.model_dump_json(indent=2))