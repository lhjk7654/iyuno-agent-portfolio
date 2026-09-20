import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.rag import ask_question


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = "gemini-3.6-flash"
QUESTIONS_FILE = Path("eval/questions.json")


def build_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    parts = []

    for i, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1,
    ):
        parts.append(
            f"[Source {i}]\n"
            f"Document: {metadata['source']}\n"
            f"Chunk: {metadata['chunk_index']}\n"
            f"{document}"
        )

    return "\n\n".join(parts)


def parse_json_response(text):
    text = text.strip()

    # 일반 JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # ```json ... ``` 형태
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 응답 안에서 { ... } 부분만 추출
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and start < end:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return None


def evaluate_faithfulness(question, answer, context):
    prompt = f"""
You are evaluating whether an AI assistant answer is supported
by the provided source context.

Question:
{question}

Source context:
{context}

Assistant answer:
{answer}

Return ONLY JSON.

The JSON must have exactly this format:

{{
  "faithful": true,
  "reason": "brief explanation"
}}

Use true only if the important claims in the answer
are supported by the source context.
"""

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            text = response.choices[0].message.content or ""
            parsed = parse_json_response(text)

            if parsed is not None:
                return parsed

            return {
                "faithful": False,
                "reason": "Evaluator returned an invalid JSON response.",
            }

        except Exception as e:
            print(f"Evaluator error (attempt {attempt + 1}/3): {e}")

            if attempt < 2:
                time.sleep(5)

    return {
        "faithful": False,
        "reason": "Evaluator API failed after 3 attempts.",
    }


def main():
    questions = json.loads(
        QUESTIONS_FILE.read_text(encoding="utf-8")
    )

    # 우선 5개만 평가
    sample = questions[:5]

    results = []

    for index, item in enumerate(sample, start=1):
        question = item["question"]

        print(f"\n[{index}/{len(sample)}] {question}")

        try:
            rag_result = ask_question(
                question,
                top_k=5,
            )

            context = build_context(
                rag_result["results"]
            )

            evaluation = evaluate_faithfulness(
                question,
                rag_result["answer"],
                context,
            )

            result = {
                "question": question,
                "faithful": bool(
                    evaluation.get("faithful", False)
                ),
                "reason": evaluation.get("reason", ""),
            }

            results.append(result)

            print(f"Faithful: {result['faithful']}")
            print(f"Reason: {result['reason']}")

        except Exception as e:
            print(f"Question failed: {e}")

            results.append(
                {
                    "question": question,
                    "faithful": False,
                    "reason": f"RAG request failed: {e}",
                }
            )

    faithful_count = sum(
        1 for item in results
        if item["faithful"]
    )

    score = faithful_count / len(results)

    print("\n" + "=" * 60)
    print("FAITHFULNESS EVALUATION")
    print("=" * 60)
    print(f"Questions: {len(results)}")
    print(f"Faithful: {faithful_count}")
    print(f"Faithfulness: {score:.3f}")

    output_file = Path(
        "eval/faithfulness_results.json"
    )

    output_file.write_text(
        json.dumps(
            results,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()