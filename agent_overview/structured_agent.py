#import libraries, you will need a requirements file for this
import nest_asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel, Field

nest_asyncio.apply()

#Define the model you would like to use
model = OpenAIModel("gpt-4")

#------------------------------------------------
# Agent with a structured response
#------------------------------------------------
"""
This example shows how to get structured, type safe responses from the agent.
- Use Pydantic modesl to define the response structure
- Type validation and safety
- Field descriptions for better model understanding
"""

#Outlines the strucure of the response you are requesting from the agent
#In this sample, we say that we want the structured response as a string as well as any escalation needs or follow up identified as a T/F
#Uses the 'Field' class to help the model understand that sentimetns should contain an analysis of the customer's emotional state and add it to the response.
#The field_examples.py file shows other ways to use the 'Field' class. 
# - Provides clean instructions to the model for data to generate
# - Helps maintain response consistency
# - Serves as documention for the data format
# - Can be used for validation 
class ResponseModel(BaseModel):
    """Structured response with metadata"""

    structured_response: str 
    needs_escalation: bool
    follow_up_required: bool
    sentiments: str = Field(description="Customer sentiment analysis")

#Similar to basic_agent. This identifies the model and system prompt.
#The added line is the result_type which calls for the strucure of the ReponseModel identified above
structured_agent = Agent(
    model=model,
    result_type=ResponseModel,
    system_prompt=(
        "You are an intelligent customer support agent."
        "Analyze queries carefully and provide a structured response"
    ),
)

#Prints the response base on the input after run_sync
structured_response = structured_agent.run_sync("I need to speak to a manager")
print(structured_response.data.model_dump_json(indent=2))