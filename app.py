import os
import sys
from pathlib import Path
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv(BASE_DIR / ".env")

from calendar_tools import get_current_datetime, list_events, create_event, TOKEN_FILE

st.set_page_config(page_title="Calendar Agent", page_icon="📅")
st.title("📅 My EventAgent")

with st.sidebar:
    st.subheader("Google Calendar Status")
    if TOKEN_FILE.exists():
        st.success("Calendar Connected ✅")
        if st.button("Disconnect Calendar"):
            try:
                TOKEN_FILE.unlink()
            except Exception:
                pass
            st.rerun()
    else:
        st.warning("Not Connected ⚠️")
        st.info("To connect Google Calendar, run this command once in your terminal:\n\n```powershell\npython auth.py\n```")
        if st.button("Check Connection Again"):
            st.rerun()

# Keep client stored in session_state to prevent garbage collection from closing httpx client
if "client" not in st.session_state:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    st.session_state.client = genai.Client(api_key=api_key) if api_key else genai.Client()

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a calendar assistant. Always call get_current_datetime first "
                "to resolve relative dates. Check list_events for conflicts before "
                "creating an event. If title, date, or time is missing, ask the user "
                "instead of guessing. Default event length is 1 hour."
            ),
            tools=[get_current_datetime, list_events, create_event],
            temperature=0,
        ),
    )
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("e.g. Schedule a project review tomorrow at 3pm"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Working..."):
            response = st.session_state.chat.send_message(prompt)
            reply = response.text or "Done."
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
