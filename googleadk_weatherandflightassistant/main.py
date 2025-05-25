import streamlit as st
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
# from agent import run_team_conversation
from agent import call_agent_async, root_agent, session_service, SESSION_ID, USER_ID, APP_NAME, session
from google.adk.memory import InMemoryMemoryService
from datetime import datetime






st.title("Google ADK Agent Integration")
st.markdown("Interact with the Google ADK agent through this UI.")

# Initialize chat history if empty
if "messages" not in st.session_state:
    st.session_state['messages'] = []

# Display all chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Delete all the items in Session state
def reset_conversation():
    if st.session_state.messages:
        del st.session_state.messages
        
# Create Runner
runner = Runner(app_name=APP_NAME,
                agent=root_agent,
                session_service=session_service,
                # memory_service=memory_service
                )
    
# Accept user input
if prompt := st.chat_input("How can I assist you today?"):
    query = f"{prompt.strip()}"
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})

    # create chat history var for whole conversation in this session 
    # chat_history = st.session_state.messages 

    
    
    # Create Chat Input Box
    with st.chat_message("user"):
        st.markdown(f"{query}")
    
    # Modify query based on memory
    # runner.agent = memory_recall_agent
    
    # if(len(memory_service.session_events)>0):
    #     query = call_agent_async(query=query,runner=runner,user_id=USER_ID, session_id=SESSION_ID)
    #     print(f"\n --  MODIFIED QUERY: {query} \n")
    
    # runner.agent=root_agent
    agent_response = call_agent_async(query=query,runner=runner,user_id=USER_ID, session_id=SESSION_ID)
    print(f"\n\nUserQuery: {query}\nAgentResponse:{agent_response}")
    
    # Add Completed Session to Memory
    # completed_session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    # memory_service.add_session_to_memory(completed_session)
    # print(f"Added session {session.id} into memory")
    
    if agent_response:
        st.markdown(agent_response)
        
    st.session_state.messages.append({"role": "assistant", "content": agent_response}) 
    
    # print("\n --SESSION EVENTS-- \n ")
    # print(session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID).events)
    # for event in session.events:
    #     print(f"Event text: {event.content.parts[0].text} in session named {session.app_name} \n")
    
    # print("\n -- Memory Session Events -- \n")
    # print(memory_service.session_events)