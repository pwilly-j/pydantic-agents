#import libraries, you will need a requirements file for this
from typing import List, Optional
import nest_asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from markdown import to_markdown

nest_asyncio.apply()

#Define the model you would like to use
model = OpenAIModel("gpt-4")

#------------------------------------------------
# Agent with a structured response & dependencies
#------------------------------------------------
"""
Shows how to use dependencies with agents
- Define complex data models with Pydantic
- Injecting runtime dependencies
- Using dynamic system prompts
- Validating inputs
"""

class ResponseModel(BaseModel):
    """Structured response with metadata"""

    structured_response: str 
    needs_escalation: bool
    follow_up_required: bool
    sentiments: str = Field(description="Customer sentiment analysis")

#define order schema
class Order(BaseModel):
    """Structure for order details"""

    order_id: str
    status: str
    items: List[str]

#define custoemr schema
class CustomerDetails(BaseModel):
    """Structure for incoming customer queries"""
    
    customer_id: str
    name: str
    email: str
    orders: Optional[List[Order]]= None

#Agent with strucutred output and dependencies
dependent_agent = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type = CustomerDetails, #sets the dependency type. Can add these details to the system prompt to make it available for the LLM
    retries = 3, 
    system_prompt=(
        "You are an intelligent customer support agent."
        "Analyze queries carefully and provide a structured response."
        "Always greet the customer when responding"
        "If the customer has ordered items, include each item as a bullet point in your response."
    ),
)

#Add dynamic systme prompt based on dependencies
@dependent_agent.system_prompt
async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
    return f"Customer details: {to_markdown(ctx.deps)}"

customer = CustomerDetails(
    customer_id="1",
    name="John Doe",
    email="john.doe@example.com",
    orders=[Order(order_id="12345",status="shipped",items=["Blue Jeans","T-Shirt",])]
)

#Calling the agent with dependencies
#The deps is identifying the customer based on the customer information provided above
"""Here's how this works
- We are giving the agent customer details
- Based on the customer details (the dependency), the agent is providing the information requested by the customer "What did I order", for their particular customer profile.
 """
response = dependent_agent.run_sync(user_prompt="What did I order?", deps=customer)
response.all_messages()
print(response.data.model_dump_json(indent=2))

#A more structured output 
print(
    "Customer Details:\n"
    f"Name: {customer.name}\n"
    f"Email: {customer.email}\n\n"
    "Response Details:\n"
    #I was getting errors with the output. The reason was that I had defined 'structured_response:' in the Reponse Model and not 'response:'
    f"{response.data.structured_response}\n\n"
    "Status:\n"
    f"Follow-up Required: {response.data.follow_up_required}\n"
    f"Needs Escalation: {response.data.needs_escalation}"
)