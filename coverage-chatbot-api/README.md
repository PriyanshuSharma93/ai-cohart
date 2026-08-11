# Coverage Chatbot API

FastAPI backend for the Coverage Chatbot project.

## Day 3 status

- `/health` - basic health check endpoint
- `/` - root info endpoint

## Setup

```bash
cd coverage-chatbot-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Visit http://127.0.0.1:8000/health