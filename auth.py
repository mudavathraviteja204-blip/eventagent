import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def authenticate():
    if not CREDENTIALS_FILE.exists():
        print(f"Error: {CREDENTIALS_FILE} not found!", flush=True)
        sys.exit(1)

    print("Initializing Google Calendar Authentication...", flush=True)
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)

    print("Starting local server on port 8080...", flush=True)
    print("Opening browser for Google sign-in...", flush=True)

    # Prompt consent & offline access ensures a persistent refresh_token is always returned
    creds = flow.run_local_server(
        port=8080,
        open_browser=True,
        prompt="consent",
        access_type="offline"
    )

    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())

    print("\nAuthentication successful!", flush=True)
    print(f"Token saved to: {TOKEN_FILE}", flush=True)
    print("You can now use your Calendar Agent in Streamlit.", flush=True)

if __name__ == "__main__":
    authenticate()
