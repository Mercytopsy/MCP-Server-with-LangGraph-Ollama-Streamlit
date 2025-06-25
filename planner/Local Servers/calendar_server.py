import os
import pickle
from datetime import datetime
from typing import Optional, List
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calendar_server")


class Calendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        self.service = self.connect_to_api()

    def connect_to_api(self):
        """Connects to Google Calendar API and returns a service client."""
        creds = None
        token_file = 'token.pickle'

        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        return build("calendar", "v3", credentials=creds)

    def get_events(self) -> List[dict]:
        """
        Retrieves calendar events between the given start and end dates (inclusive).
        

        Returns:
            List[dict]: List of matching calendar events.
        """
        start_dt = datetime.now().date()
        matched_events = []

        events_result = self.service.events().list(calendarId='primary').execute()

        for event in events_result.get('items', []):
            event_start_str = event['start'].get('dateTime') or event['start'].get('date')

            try:
                event_start_dt = datetime.fromisoformat(event_start_str).date()
            except ValueError:
                print(f"Skipping event with invalid date: {event.get('summary', 'Untitled')}")
                continue

            if event_start_dt == start_dt:
                # Matched event
                event_summary = event.get('summary', 'No Title')
                matched_events.append({
                    'start': event_start_dt,
                    'summary': event_summary
                })

        return matched_events



# cal_data = Calendar()
# print(cal_data.get_events())

@mcp.tool()
async def get_calendar_events() -> List[dict]:
    """Use this tool to retrieve calendar events"""
    try:
       cal_data = Calendar()
       return cal_data.get_events()
    except Exception as e:
        return f"Error fetching events: {e}"





# Run the MCP server locally
if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run(transport="stdio"))