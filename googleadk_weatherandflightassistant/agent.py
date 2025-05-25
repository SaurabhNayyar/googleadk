from google.adk.agents import Agent, LlmAgent
from google.adk.runners import Runner
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import ToolContext, agent_tool
from google.genai import types
from google.adk.planners import PlanReActPlanner
from google.adk.tools.agent_tool import AgentTool

from tools.weatherDetails import get_weather
from tools.countryDetails import get_country_details
from tools.flightDetails import search_flights
from tools.validateFlightRequest import validateFlightRequestDetails_beforeToolCallback

from prompts import get_root_agent_prompt

import asyncio

from dotenv import load_dotenv, find_dotenv
from datetime import datetime

# MODEL_NAME = "openai/gpt-4"
MODEL_NAME = "gemini-2.0-flash"

load_dotenv(find_dotenv(".env"))

session_service = InMemorySessionService()
# session: Session = session_service.create_session(app_name=APP_NAME,user_id=USER_ID,session_id=SESSION_ID)
# Create session
SESSION_ID=f"SESSION_001"
USER_ID = "USER_001"
APP_NAME = "WEATHER AND FLIGHT APP"
session: Session = session_service.create_session(app_name=APP_NAME,user_id=USER_ID,session_id=SESSION_ID)

# Create Memory
# memory_service = InMemoryMemoryService()

# Country Agent
country_agent=None
try:
    country_agent = Agent(name="country_agent",
                        description="Fetches information about a country.",
                        # model=LiteLlm(model=MODEL_NAME),
                        model=MODEL_NAME,
                        instruction="You are a country assistant."
                        "You return the currency, language, capital city, calling code and region about a requested country ."
                        "You MUST use 'get_country_details' tool to get the country information."
                        "If status is success, politely respond with the country information."
                        "If status is error, politely return the error message.",
                        tools=[get_country_details])
except Exception as e:
    print(f"Could not create Country agent. Check GPT Model API Key, Error:{e}")
    
# Weather Agent
weather_agent=None
try:
    weather_agent = Agent(name="weather_agent",
                        description="Fetches weather information for a city",
                        # model=LiteLlm(model=MODEL_NAME),
                        model=MODEL_NAME,
                        instruction="You are a weather assistant"
                        "You return the weather of a city mentioned by user in their request."
                        "You MUST use 'get_weather' tool to get the weather details."
                        "If status is success, politely respond with the weather information."
                        "If status is error, politely return the error message.",
                        tools=[get_weather])
except Exception as e:
    print(f"Could not create Weather agent. Check GPT Model API Key, Error:{e}")

# Flight Agent
flight_agent = None
try:
    flight_agent = Agent(name='flight_agent',
                        description='Fetches flight information between two cities',
                        # model=LiteLlm(model=MODEL_NAME),
                        model=MODEL_NAME,
                        instruction = (
                            "You are a flight search assistant."
                            "Your task is to return the available flights between two cities requested by the user."
                            "You MUST use the 'search_flights' tool to retrieve the available flight information. "
                            # "Do NOT default or assume any arguments required by 'search_flights' tool. If the flight search arguments are not clearly mentioned in the user request, politely request user for the details. For requesting these to user, you MUST use the original names of the arguments used in search_flights tool."
                            "Do NOT default or assume any arguments required by 'search_flights' tool. If the flight search arguments are not clearly mentioned in the user request, politely request user for the details. For requesting these to user, you MUST put them in bulleted list for ease of readability."
                            f"If the year for the flight search date is not mentioned in the user query, assume it is the current year ({datetime.now().year}) and notify the user that you used the current year for the search."
                            "If the search status is 'success', politely provide the requested flight information from the 'flight_info'."
                            "If the search status is 'error', look for 'message'. If 'message' contains 'missing_fields', return the list of missing fields in JSON format. Otherwise, politely return the error message to the user"
                            # "If the search status is 'error', politely return the error message to the user."
                        ),
                        before_tool_callback=validateFlightRequestDetails_beforeToolCallback,
                        tools=[search_flights],
                        )
    
except Exception as e:
    print(f"Could not create Flight agent. Check GPT Model API Key, Error{e}")

# planner = PlanReActPlanner()
# planning_instructions  = planner.build_planning_instruction()

# Root Agent
root_agent=None
if 'weather_agent' and 'flight_agent' in globals():
    root_agent = Agent(name = "root_agent",
                    # model=LiteLlm(model=MODEL_NAME),
                    model=MODEL_NAME,
                    instruction=get_root_agent_prompt(),
                    # sub_agents=[weather_agent, flight_agent],
                    tools = [AgentTool(weather_agent), AgentTool(flight_agent)],
                    planner=PlanReActPlanner()
                    )
    print(f"Root Agent {root_agent.name} created with sub agents {[sa.name for sa in root_agent.sub_agents]}")
else:
    print("Cannot create root agent because one or more sub-agents failed to initialize")
    
# Agent 2: Agent that can use memory
# memory_recall_agent = LlmAgent(
#     model=LiteLlm(model=MODEL_NAME),
#     name="MemoryRecallAgent",
#     instruction="Answer the user's question. Use the 'load_memory' tool "
#                 "if the answer might be in past conversations.",
#     tools=[load_memory], # Give the agent the tool
#     sub_agents=[root_agent]
# )
    
# Define Agent Interaction Function
def call_agent_async(query:str, runner: Runner, user_id:str, session_id:str)->str:
    content = types.Content(parts=[types.Part(text=query)],role='user')
    
    final_response_text = "Agent did not produce a final response" #Default
    
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=content):
        print(f"\n--EVENT--\n: {event}")
        print(f"\n--EVENT FINAL RESPONSE--\n: {event.is_final_response()}")
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Add more checks here if needed (e.g., specific error codes)
            break # Stop processing events once the final response is found
    
    # print(final_response_text)
    return final_response_text
        
    
# Run Conversation
"""
if 'root_agent' in globals():
    async def run_team_conversation():
        print("\n -- Testing Team Delegation --")
        # Session Service   
        session_service = InMemorySessionService()

        APP_NAME = "Weather and Flight App"
        USER_ID = "USER_001"
        SESSION_ID = "SESSION_01"
        session = session_service.create_session(app_name=APP_NAME,
                                                user_id=USER_ID,
                                                session_id=SESSION_ID)
        print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
        
        runner = Runner(agent=root_agent,
                        app_name=APP_NAME,
                        session_service=session_service)
        print("Runner created for root agent")
        
        await call_agent_async(query="I am planning to travel to Atlanta, can you help me search a flight from Minneapolis for May 30th?",
                               runner=runner,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
        print(session.events)
        await call_agent_async(query="How's the weather there?",
                               runner=runner,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
        
else:
    print("Root agent not defined")
    
async def main():
    print("Calling async function")
    result = await run_team_conversation()
    # print("Async function returned:", result)
    
asyncio.run(main())
"""