# JARVIS — Personal AI Assistant

**JARVIS (Just A Rather Very Intelligent System)** is a personal AI assistant project being built step by step with Python. The current milestone focuses on the backend foundation: conversation management, message persistence, and REST APIs. AI model integration is planned for a future milestone.

## Current Features

- FastAPI backend
- SQLite database for local conversation and message storage
- Create and list conversations
- Save and retrieve conversation messages
- Update conversation titles
- Delete conversations
- Pydantic request and response validation
- Interactive API documentation with Swagger UI

## Tech Stack

- **Language:** Python
- **Backend:** FastAPI, Uvicorn
- **Database:** SQLite
- **Validation / Settings:** Pydantic, pydantic-settings
- **Version Control:** Git and GitHub

## Project Structure

```text
JARVIS/
├── app/
│   ├── api/
│   ├── db/
│   ├── schemas/
│   └── main.py
├── requirements.txt
└── .gitignore
```

## Run Locally (Windows PowerShell)

1. Clone the repository:

   ```powershell
   git clone https://github.com/shubhamjadhav0715/JARVIS.git
   cd JARVIS
   ```

2. Create and activate a virtual environment:

   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Start the development server:

   ```powershell
   python -m uvicorn app.main:app --reload
   ```

5. Open the API documentation:

   - Swagger UI: http://127.0.0.1:8000/docs
   - Health check: http://127.0.0.1:8000/health

## Roadmap

- [ ] Integrate an online AI model through an API
- [ ] Build an AI-powered chat service
- [ ] Add voice and text interaction
- [ ] Develop memory and personalization features
- [ ] Explore offline support and cross-device access
- [ ] Add secure, permission-based task automation

## Security Notes

- Keep API keys and other secrets in environment variables; never commit them to GitHub.
- Local virtual environments, environment files, and SQLite database files are excluded through `.gitignore`.
- The current project is an actively developing prototype. The roadmap items above are planned, not implemented yet.

## Project Status

**In development** — backend foundation and conversation management APIs are implemented. AI integration is the next planned milestone.

---

Built as a learning-by-building project.
