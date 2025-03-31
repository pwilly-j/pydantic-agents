#import libraries, you will need a requirements file for this
from typing import List, Optional, Dict
import nest_asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel

from markdown import to_markdown

nest_asyncio.apply()

#Define the model you would like to use
model = OpenAIModel("gpt-4")

#------------------------------------------------
# Agent with tools
#------------------------------------------------
"""
This example shows how to enhance agents with custom tools.
Key concepts:
- Creating and registering tools
- Accessing context in tools

There are two types of tools
@agent.tool - Used for tools that need to access content from the agent. Most common.
@agent.tool.plain - Tools that don't need to access the agent context

Tools can be registerd in two different ways
1. Use the @ decorator
2. In the agent definition, provide a list of tools
"""

#Creates a class to structure the way the LLM response to us. 
#When the LLM responds it will include all of these outputs
class ResponseModel(BaseModel):
    structured_response: str 
    needs_escalation: bool
    follow_up_required: bool
    sentiments: str = Field(description="Customer sentiment analysis")

#Creates a class for the strucutre of an order
#Orders will include an ID, status, and items
class Order(BaseModel):
    order_id: str
    status: str
    items: List[str]

#Creates a class for the customer detail structure
#Every customer will have an ID, name, email, and their orders
class CustomerDetails(BaseModel):
    """Structure for incoming customer queries"""
    
    customer_id: str
    name: str
    email: str
    orders: Optional[List[Order]]= None
    #Optional indicates that a customer may or may not have orders
    #=None sets the default to None if there are no orders

customer = CustomerDetails(
    customer_id="1",
    name="John Doe",
    email="john.doe@example.com",
    orders=[Order(order_id="12345",status="shipped",items=["Blue Jeans","T-Shirt",])]
)

#In a traditional tool this would be calling an API or some other kind of database
#Normally, this would not be in the code base, in this case we are just building a simple dictionary
shipping_info_db: Dict[str, str] = {
    "12345": "Shipped on 2024-12-01",
    "67890": "Out for delivery",
}

#This is a tool that will be used to get the shipping information for the customer 
def get_shipping_info(ctx: RunContext[CustomerDetails]) -> str:
    """Get the customer's shipping information."""
    return shipping_info_db [ctx.deps.orders[0].order_id]
    #ctx is based on on what is defined in the dependency above in this case it is the customer details 
    #ctx.deps indicates the dependency, in this case it is the customer details, this is also identified in the agent_6 below using the deps_type
    #ctx.deps.orders accesses the orders from the customer details which is defined in the CustomerDetails class above
    #orders[0] accesses the first order from the customer details
    #order_id = 12345 is then used to access the shipping information from the shipping_info_db dictionary
    #The shipping information is then returned to the agent which would be "Shipped on 2024-12-01"


#Agent with structured output and dependencies
agent_6 = Agent(
    #model is idenfied above, you can also just call out the speicific model here
    model=model,
    #Sets the result (output) to the ResponseModel identified above with a structures response, escalation, etc.
    result_type=ResponseModel,
    #Sets the dependency type. These details are added to the system prompt to make it available for the LLM 
    #In this case, the only additional dependency being added here is the Customer Details data below with information for John Doe
    deps_type = CustomerDetails,
    #Specifies how many times to retry if the agent fails
    #Failures can be due to API issues, network timeouts, rate limits
    #Useful when working with external APIs (like OpenAI in this case) where temporary issues are common.   
    retries = 3,
    #Gives the agent a specific set of responsibilities
    system_prompt=(
        "You are an intelligent customer support agent."
        "Analyze queries carefully and provide a structured response."
        "Always greet the customer when responding"
        "If the customer has ordered items, include each item as a bullet point in your response."
        "Use tools to look up relevant information"
    ),
    #Makes the get_shipping_info tool available to the agent 
    #Takes_ctx=True indicates that the tool will need the context of the agent 
    tools=[Tool(get_shipping_info,takes_ctx=True)],
)

#Add dynamic systme prompt based on dependencies
@agent_6.system_prompt
async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
    return f"Customer details: {to_markdown(ctx.deps)}"

#Calling the agent with dependencies
#The deps is identifying the customer based on the customer information provided above
"""Here's how this works
- We are giving the agent customer details
- Based on the customer details (the dependency), the agent is providing the information requested by the customer "What did I order", for their particular customer profile.
 """
response = agent_6.run_sync(user_prompt="What is the status of my last order?", deps=customer)

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