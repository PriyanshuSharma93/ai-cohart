"""
chatbot.py - Day 3 local CLI chatbot using Ollama
"""

import sys
from ollama import chat

MODEL_NAME = "llama3.2"

SYSTEM_PROMPT = (
    "You are a friendly, concise assistant helping someone learn AI "
    "engineering. Keep answers clear and not too long."
)


def run_chat() -> None:
    print("=== Local Ollama Chatbot ===")
    print(f"Model: {MODEL_NAME}")
    print("Type 'exit' or 'quit' to stop.\n")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            response = chat(model=MODEL_NAME, messages=messages)
        except Exception as e:
            print(f"\n[Error talking to Ollama: {e}]")
            print("Is Ollama running? Try `ollama serve` in another terminal.\n")
            messages.pop()
            continue

        reply = response["message"]["content"]
        print(f"Bot: {reply}\n")

        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    sys.exit(run_chat() or 0)