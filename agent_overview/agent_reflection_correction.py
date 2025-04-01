#import libraries, you will need a requirements file for this
from typing import List, Optional, Dict
import nest_asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Tool, ModelRetry
from pydantic_ai.models.openai import OpenAIModel

import markdown

nest_asyncio.apply()

#Define the model you would like to use
model = OpenAIModel("gpt-4")

#------------------------------------------------
# Agent with Reflection and Correction
#------------------------------------------------
"""
This example demonstrates advanced agent capabilities with self-correction.
Key concepts:
- Implementing self-reflection
- Handling errors gracefully with retries
- Using ModelRetry for automatic retries
- Decorator-based tool registration
"""

class ResponseModel(BaseModel):
    structured_response: str 
    needs_escalation: bool
    follow_up_required: bool
    sentiments: str = Field(description="Customer sentiment analysis")

class Order(BaseModel):
    order_id: str
    status: str
    items: List[str]

class CustomerDetails(BaseModel):
    """Structure for incoming customer queries"""
    
    customer_id: str
    name: str
    email: str
    orders: Optional[List[Order]]= None

shipping_info_db: Dict[str, str] = {
    "#12345": "Shipped on 2024-12-01",
    "#67890": "Out for delivery",
}

customer = CustomerDetails(
    customer_id="1",
    name="John Doe",
    email="john.doe@example.com",
)

agent_6 = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type = CustomerDetails,
    retries = 3,
    system_prompt=(
        "You are an intelligent customer support agent."
        "Analyze queries carefully and provide a structured response."
        "Always greet the customer when responding"
        "Use tools to look up relevant information"
        #The ModelRety was not working and was asking the customer to provide a corrected order ID with a hashtag. 
        #To get the ModelRetry to work properly, we added the following to the system prompt: 
        "When a tool raises ModelRetry, handle it internally by correcting the input and retrying."
        "Never expose technical details like ModelRetry or hashtag requirements to the customer."
        "Always provide a clean, user-friendly response with the requested information."
    ),
)

#This is a tool that will be used to get the shipping information for the customer 
#We are using the plain tool because we are not using a tool call based on context from the agent
@agent_6.tool_plain()
def get_shipping_status(order_id: str) -> str:
    """Get the shipping status for a given order ID."""
    shipping_status = shipping_info_db.get(order_id)
    if shipping_status is None:
        #ModelRetry can be used to handle errors
        #In this case, a common error in the system might be that the order ID does not include a hashtag. This is what the if statement addresses above. 
        #In the ModelRetry, we are telling the LLM to self correct the error by adding a hashtag to the order ID and then trying again. 
        raise ModelRetry(
            f"No shipping information found for order ID: {order_id}."
            "Make sure the order ID starts with '#'"
            "Self correct this if needed and try"
        )
    return shipping_info_db [order_id]

#Add dynamic systme prompt based on dependencies
@agent_6.system_prompt
async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
    return f"Customer details: {markdown.to_markdown(ctx.deps)}"

response = agent_6.run_sync(
    user_prompt="What is the status of my last order 12345?", deps=customer)

response.all_messages()
print(response.data.model_dump_json(indent=2))
