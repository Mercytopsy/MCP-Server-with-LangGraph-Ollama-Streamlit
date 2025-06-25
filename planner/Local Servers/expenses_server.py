from datetime import datetime
from uuid import uuid4
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Union, Any
import psycopg2
import os
load_dotenv()


# Initialize the MCP server with a name
mcp = FastMCP("expense_tracker_server")
  

DB_CONFIG = dict(
    host=os.getenv("DB_HOST"),   
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=5432
)

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)




def fetch_query(query, params=None):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

def execute_query(query, params=None):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            conn.commit()

@mcp.tool()
async def get_all_expenses() ->list[dict[str, Any]]:
    """Use this tool to search for all expenses"""
    try:
        query = "SELECT * FROM expenses"
        return fetch_query(query)
    except Exception as e:
        return f"Error fetching expenses: {e}"

@mcp.tool()
def save_expense_to_db(title: str, amount: Union[int, float]) -> str:
    """
    Use this tool to save user's expense by title and amount to database.
    """
    try:
        insert_query = """
            INSERT INTO expenses (id, title, amount, date)
            VALUES (%s, %s, %s, %s)
        """
        params = (str(uuid4()), title, amount, datetime.utcnow().date())
        execute_query(insert_query, params)
        return "Your expense has been saved successfully."
    except Exception as e:
        return f"Failed to save expense: {e}"




# Run the MCP server locally
if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run(transport="stdio"))