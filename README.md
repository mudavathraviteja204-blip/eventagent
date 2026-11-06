# 📅 AI Calendar Agent

An intelligent, conversational Calendar Assistant powered by **Google Gemini 2.5 Flash**, **Streamlit**, and the **Google Calendar API**.

The agent understands natural language, resolves relative dates (like *"tomorrow at 3pm"* or *"next Monday morning"*), checks for scheduling conflicts on your calendar, and books events directly to your primary Google Calendar.

---

## ✨ Features

- **Natural Language Event Scheduling**: Simply type *"Schedule project review tomorrow at 3pm"* and the agent handles the rest.
- **Smart Conflict Detection**: The agent automatically queries Google Calendar to verify your availability before creating new events.
- **Relative Date & Time Resolution**: Understands *"today"*, *"tomorrow"*, and specific days of the week in your local timezone (`Asia/Kolkata`).
- **Interactive Web Interface**: Clean chat interface built with Streamlit.
- **Secure OAuth 2.0 Flow**: Direct Google OAuth with offline refresh token support so credentials never expire.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LLM**: Google Gemini (`google-genai` SDK)
- **UI**: Streamlit
- **Calendar**: Google Calendar API v3 (`google-api-python-client`)
- **Auth**: `google-auth-oauthlib`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/calendar-event-agent.git
cd calendar-event-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Google Cloud & API Keys

1. **Gemini API Key**: Get your API key from [Google AI Studio](https://aistudio.google.com/).
2. **Google Calendar OAuth**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Enable **Google Calendar API**.
   - Create an **OAuth 2.0 Client ID** (Web application or Desktop application).
   - Under **Authorized redirect URIs**, add:
     ```text
     http://localhost:8080/
     http://localhost:8080
     ```
   - Download the client secrets file and save it as `credentials.json` in this folder.

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Add your keys in `.env`:
   ```env
   GOOGLE_API_KEY="your_gemini_api_key"
   CLIENT_ID="your_google_client_id"
   CLIENT_SECRET="your_google_client_secret"
   ```

---

## 🔑 One-Time Authentication

Run the authentication script once to connect your Google Calendar:

```bash
python auth.py
```

This opens your browser to grant calendar access and saves `token.json` locally.

---

## 🖥️ Run the Application

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and start chatting with your calendar assistant!

---

## 📂 Project Structure

```text
├── app.py              # Streamlit chat interface and Gemini agent setup
├── calendar_tools.py   # Google Calendar tool functions (get_time, list, create)
├── auth.py             # One-time Google OAuth authorization script
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Keeps secrets and tokens out of version control
└── README.md           # Project documentation
```

---

## 🔒 Security Note

Never commit `.env`, `credentials.json`, or `token.json` to version control. They are listed in `.gitignore` by default to keep your credentials safe.
