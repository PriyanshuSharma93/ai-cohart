"""
coverage-chatbot-api/main.py
FastAPI skeleton for the Coverage Chatbot backend.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Coverage Chatbot API",
    description="Backend API for the Coverage Chatbot project.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "coverage-chatbot-api"}


@app.get("/")
def root():
    return {"message": "Coverage Chatbot API is running. See /docs for details."}