import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.tools import search_documents


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY") or "test-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=30.0,
)


MODEL = "gemini-3.5-flash-lite"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": (
                "Search the cybersecurity and AI document collection. "
                "Use this tool when answering questions that require "
                "information from the indexed NIST documents."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query.",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of documents to retrieve.",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        },
    }
]


def run_agent(question: str) -> dict:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a cybersecurity and AI risk assistant. "
                "Use the search_documents tool when you need information "
                "from the indexed NIST documents. "
                "Answer using the retrieved evidence and do not invent facts."
            ),
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    response = client.chat.completions.create(
        model=MODEL,
        reasoning_effort="low",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    message = response.choices[0].message

    tool_results = []

    if message.tool_calls:
        messages.append(message)

        for tool_call in message.tool_calls:
            if tool_call.function.name == "search_documents":
                arguments = json.loads(tool_call.function.arguments)

                query = arguments["query"]
                top_k = arguments.get("top_k", 5)

                result = search_documents(
                    query=query,
                    top_k=top_k,
                )

                tool_results.append(result)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )

        final_response = client.chat.completions.create(
            model=MODEL,
            reasoning_effort="low",
            messages=messages,
        )

        answer = final_response.choices[0].message.content

    else:
        answer = message.content

    return {
        "answer": answer,
        "tool_used": bool(message.tool_calls),
        "tool_results": tool_results,
    }


if __name__ == "__main__":
    print("=== Iyuno AI Agent ===")

    question = input("\n질문을 입력하세요: ")

    result = run_agent(question)

    print("\n=== Answer ===")
    print(result["answer"])

    print("\n=== Tool Used ===")
    print(result["tool_used"])

    if result["tool_results"]:
        print("\n=== Tool Result ===")
        print(json.dumps(result["tool_results"], indent=2, ensure_ascii=False))