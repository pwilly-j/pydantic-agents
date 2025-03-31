#import libraries, you will need a requirements file for this
import nest_asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

nest_asyncio.apply()

#Define the model you would like to use
model = OpenAIModel("gpt-4o")

#Define basic agent parameters
basic_agent = Agent(
    model=model,
    system_prompt="You are a helpful customer support agent. Be concise and friendly."
)

response = basic_agent.run_sync("How can I track my order #12345")
print(response.data)
print(response.all_messages())
#print(response.cost())