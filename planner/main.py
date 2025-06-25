import streamlit as st
from graph import create_agent
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
import asyncio
import uuid
import logging

import sys, asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(page_title="AI Daily Planner", layout="centered")




st.title("AI Daily Planner")
logging.info("App started")


  

if 'messages' not in st.session_state:
   st.session_state.messages = [
    {
        "role": "assistant",
        "content": (
            "Hi there! I'm your **AI Daily Planner**.\n\n"
            "I can help you with:\n"
            "- 📅 Managing your calendar\n"
            "- 💸 Tracking your expenses\n"
            "- 🌦️ Getting real-time weather updates\n\n"
            "Just ask me anything like:\n"
            "• *What's the weather in Lagos today?*\n"
            "• *List all my expenses this month.*\n"
            "• *Do I have any meetings scheduled?*\n\n"
            "Let's get started! 🚀"
        )
    }
]
# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_prompt = st.chat_input("Your question")

# On user message
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Stream assistant response
    with st.chat_message("assistant"):
        logging.info("Generating response...")
        with st.spinner("Processing..."):   
            response_placeholder = st.empty()

            async def run_chat():
                graph, _ = await create_agent()
                inputs = {
                    "messages": [HumanMessage(content=user_prompt)]
                }
                config = {"configurable": {"thread_id": str(uuid.uuid4())}}
                all_text_output=[]
                async for output in graph.astream(inputs, config=RunnableConfig(config)):
                    for node_name, msg_content in output.items():
                        for msg in msg_content.get("messages", []):
                            #Handle Assistant (AI) Message
                            if isinstance(msg, AIMessage):
                                all_text_output.append(msg.content)
                            #Handle Tool Response
                            elif isinstance(msg, ToolMessage):
                                all_text_output.append(
                                "\n```json\n 🔧MCP Tool Name:" + str(msg.name) + "\n```\n"
                                )
                                
                    response_placeholder.markdown("".join(all_text_output))
                        
    
    

                return "".join(all_text_output)

            assistant_output = asyncio.run(run_chat())

            st.session_state.messages.append({"role": "assistant", "content": assistant_output})