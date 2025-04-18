from google.adk.agents import Agent
from google.adk.memory import InMemoryMemoryService
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
"""The Runner class is used to run agents.
It manages the execution of an agent within a session, handling message processing, 
event generation, and interaction with various services like artifact storage, 
session management, and memory."""
from google.genai import types

import warnings
#Ignore all warnings
warnings.filterwarnings("ignore")

# @title Define the get_weather Tool
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    # Best Practice: Log tool execution for easier debugging
    print(f"--- Tool: get_weather called for city: {city} ---")
    city_normalized = city.lower().replace(" ", "") # Basic input normalization

    # Mock weather data for simplicity
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }

    # Best Practice: Handle potential errors gracefully within the tool
    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}

# Example tool usage (optional self-test)
# print(get_weather("New York"))
# print(get_weather("Paris"))

weather_agent = Agent(
    name = "weather_agent_v1",
    model=LiteLlm("openai/o4-mini"),
    description="Provides weather information for specific cities.", # Crucial for delegation later
    instruction="You are a helpful weather assistant. Your primary goal is to provide current weather reports. "
                "When the user asks for the weather in a specific city, "
                "you MUST use the 'get_weather' tool to find the information. "
                "Analyze the tool's response: if the status is 'error', inform the user politely about the error message. "
                "If the status is 'success', present the weather 'report' clearly and concisely to the user. "
                "Only use the tool when a city is mentioned for a weather request.",
    tools=[get_weather], # Make the tool available to this agent
)

"""
SessionService: Responsible for managing conversation history and 
state for different users and sessions. 
The InMemorySessionService is a simple implementation that stores everything in memory, 
suitable for testing and simple applications
"""
session_service = InMemorySessionService()

APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID="session_001"

session = session_service.create_session(app_name=APP_NAME,
                                         user_id=USER_ID,
                                         state={},
                                         session_id=SESSION_ID)

"""
Runner: The engine that orchestrates the interaction flow. 
It takes user input, routes it to the appropriate agent,
manages calls to the LLM and tools based on the agent's logic, 
handles session updates via the SessionService, 
and yields events representing the progress of the interaction.
"""

runner = Runner(app_name=APP_NAME,
                agent=weather_agent,
                session_service=session_service,
                # memory_service=
                )

"""
Since LLM calls and tool executions can take time, ADK's Runner operates asynchronously.
"""
import asyncio
from google.genai import types

async def call_agent_async(query:str):
    """Sends a user query to the agent and prints a final response"""

    #Prepare User Query in ADK format
    content = types.Content(parts=[types.Part(text=query)], role='user')

    final_response_text = "No response from agent"

    # Call Runner Async
    async for event in runner.run_async(user_id=USER_ID,session_id=SESSION_ID,new_message=content):
        # You can uncomment the line below to see *all* events during execution
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: #handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No Specific Error Message'}"
    
    print(f"Agent Response: {final_response_text}")


# Run the conversation
async def run_conversation():
    await call_agent_async("How is the weather in London?")
    await call_agent_async("How about New York?")
    await call_agent_async("and Tokyo?")

async def main():
    print("Calling async function")
    result = await run_conversation()
    # print("Async function returned:", result)
    
asyncio.run(main())
