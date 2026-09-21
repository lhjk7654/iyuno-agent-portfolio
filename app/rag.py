import os
import time

from dotenv import load_dotenv
from openai import OpenAI

from app.retriever import search


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY") or "test-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=30.0,
)

MODEL = "gemini-3.5-flash-lite"


def build_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for i, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1,
    ):
        source = metadata["source"]
        chunk = metadata["chunk_index"]

        context_parts.append(
            f"[Source {i}]\n"
            f"Document: {source}\n"
            f"Chunk: {chunk}\n"
            f"Content:\n{document}"
        )

    return "\n\n".join(context_parts)


def ask_question(question: str, top_k: int = 5):
    # 1. Retrieval
    retrieval_start = time.perf_counter()

    print("\n[1/3] Searching documents...")

    results = search(question, top_k=top_k)

    retrieval_latency = time.perf_counter() - retrieval_start

    print(f"[1/3] Retrieval completed: {retrieval_latency:.3f}s")

    # 2. Build context
    context = build_context(results)

    print("[2/3] Context built.")

    prompt = f"""
You are a cybersecurity and AI risk assistant.

Answer the user's question using ONLY the provided source context.

Rules:
1. Do not invent information.
2. If the context does not contain enough information,
   say that the documents do not provide enough information.
3. Explain the answer clearly.
4. At the end, provide a Sources section.
5. In the Sources section, list the document name
   and chunk number used for the answer.

User question:
{question}

Source context:
{context}
"""

    # 3. Gemini
    llm_start = time.perf_counter()

    print("[3/3] Sending request to Gemini...")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            reasoning_effort="low",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

    except Exception as e:
        print(f"[3/3] Gemini request failed: {e}")

        return {
            "answer": f"Gemini API 요청 중 오류가 발생했습니다.\n\n{e}",
            "retrieval_latency": retrieval_latency,
            "llm_latency": time.perf_counter() - llm_start,
            "total_latency": time.perf_counter() - retrieval_start,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "results": results,
        }

    llm_latency = time.perf_counter() - llm_start

    print(f"[3/3] Gemini response received: {llm_latency:.3f}s")

    answer = response.choices[0].message.content

    usage = response.usage

    prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
    completion_tokens = getattr(usage, "completion_tokens", 0) or 0
    total_tokens = getattr(usage, "total_tokens", 0) or 0

    return {
        "answer": answer,
        "retrieval_latency": retrieval_latency,
        "llm_latency": llm_latency,
        "total_latency": retrieval_latency + llm_latency,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "results": results,
    }


def main():
    print("=== Iyuno AI Security RAG ===")

    question = input("\n질문을 입력하세요: ")

    result = ask_question(question)

    print("\n=== Answer ===")
    print(result["answer"])

    print("\n=== Performance ===")
    print(f"Prompt tokens:     {result['prompt_tokens']}")
    print(f"Completion tokens: {result['completion_tokens']}")
    print(f"Total tokens:      {result['total_tokens']}")
    print(f"Retrieval latency: {result['retrieval_latency']:.3f}s")
    print(f"LLM latency:       {result['llm_latency']:.3f}s")
    print(f"Total latency:     {result['total_latency']:.3f}s")


if __name__ == "__main__":
    main()