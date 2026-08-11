"""
main.py - Day 3 first AI-assisted Python script
"""

def get_fun_facts(topic: str) -> list[str]:
    return [
        f"{topic} is something people are curious about.",
        f"There's always more to learn about {topic}.",
        f"You just wrote your first AI-assisted Python script about {topic}!",
    ]


def main() -> None:
    print("=== Day 3: My First Python Project ===")
    topic = input("Enter a topic you're curious about: ").strip()

    if not topic:
        print("You didn't enter anything - defaulting to 'Python'.")
        topic = "Python"

    facts = get_fun_facts(topic)

    print(f"\nHere's what I've got on '{topic}':")
    for i, fact in enumerate(facts, start=1):
        print(f"  {i}. {fact}")


if __name__ == "__main__":
    main()