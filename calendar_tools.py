import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.json"
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
ENV_FILE = BASE_DIR / ".env"

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TZ = "Asia/Kolkata"

load_dotenv(ENV_FILE)

def _service():
    if not TOKEN_FILE.exists():
        raise RuntimeError(
            "Google Calendar not connected! Please run 'python auth.py' once in your terminal to sign in."
        )

    try:
        with open(TOKEN_FILE, "r") as f:
            info = json.load(f)

        creds = Credentials(
            token=info.get("token"),
            refresh_token=info.get("refresh_token"),
            token_uri=info.get("token_uri", "https://oauth2.googleapis.com/token"),
            client_id=info.get("client_id"),
            client_secret=info.get("client_secret"),
            scopes=info.get("scopes", SCOPES),
        )
    except Exception as e:
        raise RuntimeError(f"Could not read token.json: {e}. Run 'python auth.py' to reconnect.")

    if not creds.valid:
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_FILE, "w") as f:
                    f.write(creds.to_json())
            except Exception as e:
                raise RuntimeError(f"Token refresh failed: {e}. Run 'python auth.py' to reconnect.")
        elif creds.token:
            # Token is available; test if valid or let Google API handle it
            pass
        else:
            raise RuntimeError("Credentials expired. Run 'python auth.py' to reconnect.")

    return build("calendar", "v3", credentials=creds)

def get_current_datetime() -> str:
    """Get the current date, day of week, and time. Call this first to resolve
    words like 'today', 'tomorrow', or 'next Friday'."""
    return datetime.now(ZoneInfo(TZ)).strftime("%A, %Y-%m-%d %H:%M (%Z)")

def list_events(date: str) -> str:
    """List calendar events on a given day.

    Args:
        date: Day in YYYY-MM-DD format, e.g. "2026-11-06".
    """
    try:
        start = datetime.fromisoformat(date).replace(tzinfo=ZoneInfo(TZ))
        end = start + timedelta(days=1)
        result = _service().events().list(
            calendarId="primary",
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        events = result.get("items", [])
        if not events:
            return f"No events on {date}."
        return "\n".join(
            f"- {e['summary']} at {e['start'].get('dateTime', e['start'].get('date'))}"
            for e in events
        )
    except Exception as e:
        return f"Failed to list events: {e}"

def create_event(title: str, start: str, end: str, description: str = "") -> str:
    """Create an event in the user's Google Calendar.

    Args:
        title: Event title, e.g. "Team meeting".
        start: Start time in ISO 8601, e.g. "2026-11-06T15:00:00".
        end: End time in ISO 8601, e.g. "2026-11-06T16:00:00".
        description: Optional notes for the event.
    """
    event = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start, "timeZone": TZ},
        "end": {"dateTime": end, "timeZone": TZ},
    }
    try:
        created = _service().events().insert(calendarId="primary", body=event).execute()
        return f"Created '{created['summary']}': {created['htmlLink']}"
    except Exception as e:
        return f"Failed to create event: {e}"
