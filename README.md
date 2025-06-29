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


### 📦 Installation & Setup

#### 🔗 Connect to Google Calendar API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. **Enable Google Calendar API**:
   - Navigate to `APIs & Services > Library`
   - Search for **Google Calendar API** and click **Enable**
4. **Configure OAuth consent screen**:
   - Go to `APIs & Services > OAuth consent screen`
   - Select user type and complete the required fields
5. **Create OAuth Client ID**:
   - Go to `APIs & Services > Credentials`
   - Click **Create Credentials > OAuth client ID**
   - Choose **Desktop app** as the application type
   - Click **Create**
6. **Download the JSON file** and rename it to:
   ```bash
   credentials.json


#### 1. Clone the repository
```bash
git clone https://github.com/Mercytopsy/MCP-Server-with-LangGraph-Ollama-Streamlit
cd MCP-Server-with-LangGraph-Ollama-Streamlit
```
#### 2. Install uv for Windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" 
```
#### 3. Create & Activate Virtual Environment
```bash
uv venv
.venv\scripts\activate.bat
```
#### 4. Install Project Dependencies
```bash
uv pip install .
```
#### 5. Navigate to the planner Directory
```bash
cd planner
```
#### 6. Copy credentials.json to this directory
```bash
copy %USERPROFILE%\Downloads\credentials.json .
```
#### 7. Run the App
```bash
streamlit run main.py
```
