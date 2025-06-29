## Build a Local MCP Server with LangGraph, Ollama & Streamlit

This project demonstrates an AI Daily Planner powered by a Local MCP (Modular Command Protocol) Server, integrating LangGraph, Ollama, and Streamlit for an interactive AI experience. It showcases how the LangGraph agent can communicate with different MCP tools (Weather, Expense, Calendar) to perform real-time, task-based planning.

![My Image](https://github.com/Mercytopsy/MCP-Server-with-LangGraph-Ollama-Streamlit/blob/main/docs/architecture%20diagram.png)


### 🧩 MCP Server
The system uses 3 different local MCP Servers:

| Server              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------------------------|
| **Weather Server**  | Integrates with the [WeatherAPI](https://www.weatherapi.com/) to fetch real-time weather data. |
| **Expense Tracker Server**  | allows users to add and retrieve expense records.              |
| **Calendar Server** | Interfaces with the user's calendar API to fetch upcoming events and appointments.             |


### ⚙️Features
- LangChain MCP Adaptors: Convert MCP tools into LangChain tools
- MCP Protocol: Standardized tool calls over stdio
- LangGraph Agent: Executes structured reasoning across tools
- Chat Interface: Interact through a simple Streamlit UI


### 🛠️ Technologies Used

| TECH STACK        | PURPOSE                             |
|-------------------|-------------------------------------|
| Python            | Core language for backend and logic |
| FastMCP           | For building MCP Servers            |
| LangGraph         | For building the agent state        |
| LangChain         | for Tool orchestration              |
| PostgreSQL        | Local database to store user expenses |
| Qwen2.5:14b       | for agent reasoning                 |
| Streamlit         | Frontend UI for user interaction    |

### 📸 Project Demo
![My Image](https://github.com/Mercytopsy/MCP-Server-with-LangGraph-Ollama-Streamlit/blob/main/docs/demo_screenshot.png)
