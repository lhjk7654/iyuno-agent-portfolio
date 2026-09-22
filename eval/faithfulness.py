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
    timeout=30.0,
)


MODEL = "gemini-3.5-flash-lite"
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

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(
        r"```json\s*(.*?)\s*```",
        text,
        re.DOTALL,
    )

    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and start < end:
        try:
            return json.loads(
                text[start:end + 1]
            )
        except json.JSONDecodeError:
            pass

    return None


def evaluate_faithfulness(
    question,
    answer,
    context,
):
    prompt = f"""
You are evaluating whether an AI assistant answer
is supported by the provided source context.

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
                reasoning_effort="low",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            text = (
                response.choices[0]
                .message.content
                or ""
            )

            parsed = parse_json_response(text)

            if parsed is not None:
                return {
                    "success": True,
                    "faithful": bool(
                        parsed.get("faithful", False)
                    ),
                    "reason": parsed.get(
                        "reason",
                        "",
                    ),
                }

            return {
                "success": False,
                "faithful": None,
                "reason": (
                    "Evaluator returned "
                    "invalid JSON."
                ),
            }

        except Exception as e:
            print(
                f"Evaluator error "
                f"(attempt {attempt + 1}/3): {e}"
            )

            if attempt < 2:
                time.sleep(5)

    return {
        "success": False,
        "faithful": None,
        "reason": (
            "Evaluator API failed "
            "after 3 attempts."
        ),
    }


def main():
    questions = json.loads(
        QUESTIONS_FILE.read_text(
            encoding="utf-8"
        )
    )

    # Start with 5 questions because
    # Gemini API quota may be limited.
    sample = questions[:5]

    results = []

    for index, item in enumerate(
        sample,
        start=1,
    ):
        question = item["question"]

        print(
            f"\n[{index}/{len(sample)}] "
            f"{question}"
        )

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
                "success": evaluation["success"],
                "faithful": evaluation["faithful"],
                "reason": evaluation["reason"],
            }

            results.append(result)

            if evaluation["success"]:
                print(
                    f"Faithful: "
                    f"{evaluation['faithful']}"
                )
                print(
                    f"Reason: "
                    f"{evaluation['reason']}"
                )
            else:
                print(
                    "Evaluation failed. "
                    "This question will not "
                    "be included in the score."
                )

        except Exception as e:
            print(
                f"RAG request failed: {e}"
            )

            results.append(
                {
                    "question": question,
                    "success": False,
                    "faithful": None,
                    "reason": (
                        f"RAG request failed: {e}"
                    ),
                }
            )

        # Avoid hitting the free-tier
        # requests-per-minute limit.
        if index < len(sample):
            time.sleep(13)

    evaluated = [
        item
        for item in results
        if item["success"]
    ]

    faithful_count = sum(
        1
        for item in evaluated
        if item["faithful"]
    )

    if evaluated:
        score = (
            faithful_count
            / len(evaluated)
        )
    else:
        score = None

    print("\n" + "=" * 60)
    print("FAITHFULNESS EVALUATION")
    print("=" * 60)

    print(
        f"Questions attempted: "
        f"{len(results)}"
    )

    print(
        f"Successfully evaluated: "
        f"{len(evaluated)}"
    )

    print(
        f"Faithful: "
        f"{faithful_count}"
    )

    if score is not None:
        print(
            f"Faithfulness: "
            f"{score:.3f}"
        )
    else:
        print(
            "Faithfulness: "
            "NOT AVAILABLE"
        )

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

    print(
        f"Saved: {output_file}"
    )


if __name__ == "__main__":
    main()