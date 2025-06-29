from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage 
from langgraph.graph.message import add_messages 
from langchain_ollama import ChatOllama

from typing import Annotated,Sequence, TypedDict
from datetime import datetime

import asyncio
# # Set event loop policy for Windows
import sys
python_path = sys.executable

# Load environment variables
load_dotenv()



# Define the LLM

llama_model = ChatOllama(model="llama3.1:latest")
qwen_model = ChatOllama(model="qwen2.5:7b")


SYSTEM_PROMPT = f"""
Today is {datetime.now().strftime("%Y-%m-%d")}
You are a smart agent with an ability to use tools. 
You will be given a question and you will use the tools to answer the question.
Pick the most relevant tool to answer the question. 
Your answer should be very polite and professional.
"""


class AgentState(TypedDict):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]



async def create_agent():
    client = MultiServerMCPClient({
        "calendar_server": {
            "command": "python",
            "args": ["C:\\Users\\.....\\planner\\Local Servers\\calendar_server.py"],
            "transport": "stdio"
        },

        
        "expense_tracker_server": {
            "command": "python",
            "args": ["C:\\Users\\.....\\planner\\Local Servers\\expenses_server.py"],
            "transport": "stdio"
        },
        "weather_server": {
            "command": "python",
            "args": ["C:\\Users\\......\\planner\\Local Servers\\weather_server.py"],
            "transport": "stdio"
        },
    })

    tools = await client.get_tools()
    print(tools)

 
    async def chatbot_node(state: AgentState):
        assistant_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("placeholder", "{messages}")
        ])
        assistant_runnable = assistant_prompt | gpt_model.bind_tools(tools)
        response = await assistant_runnable.ainvoke({"messages": state["messages"]})
        return {"messages": [response]}

    workflow = StateGraph(AgentState)
    workflow.add_node("chatbot_node", chatbot_node)
    workflow.add_node(ToolNode(tools))
    workflow.add_edge(START, "chatbot_node")
    workflow.add_conditional_edges("chatbot_node", tools_condition)
    workflow.add_edge("tools", "chatbot_node")
    graph = workflow.compile(checkpointer=MemorySaver())

    return graph, client





