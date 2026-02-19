"""
CLI version of HR Chatbot using the core module.
"""
from collections import deque
from hr_core import get_response


def chat():
    print("\nHR Support Chatbot (type 'exit' to quit)\n")

    # session memory: keep the last 10 exchanges (question, answer)
    memory = deque(maxlen=10)

    while True:
        question = input("Employee: ")
        if question.lower() == "exit":
            break

        response = get_response(question, memory)

        print("\nHR Bot:", response)
        print("-" * 60)

        # append this exchange to session memory
        memory.append((question, response))


if __name__ == "__main__":
    chat()
