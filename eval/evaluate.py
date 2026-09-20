import json
import time
from pathlib import Path

from app.retriever import search


QUESTIONS_FILE = Path("eval/questions.json")


def evaluate_question(question: str, expected_source: str, top_k: int):
    start = time.perf_counter()

    results = search(question, top_k=top_k)

    elapsed = time.perf_counter() - start

    sources = [
        metadata["source"]
        for metadata in results["metadatas"][0]
    ]

    hit = expected_source in sources

    return hit, elapsed, sources


def main():
    questions = json.loads(
        QUESTIONS_FILE.read_text(encoding="utf-8")
    )

    results = []

    for index, item in enumerate(questions, start=1):
        question = item["question"]
        expected_source = item["source"]

        hit1, latency, sources1 = evaluate_question(
            question,
            expected_source,
            top_k=5,
        )

        hit3 = expected_source in sources1[:3]
        hit5 = expected_source in sources1[:5]

        results.append({
            "question": question,
            "expected_source": expected_source,
            "recall_at_1": int(
                expected_source in sources1[:1]
            ),
            "recall_at_3": int(hit3),
            "recall_at_5": int(hit5),
            "latency_seconds": round(latency, 4),
        })

        print(
            f"[{index:02d}/{len(questions)}] "
            f"R@1={int(expected_source in sources1[:1])} "
            f"R@3={int(hit3)} "
            f"R@5={int(hit5)} "
            f"Latency={latency:.3f}s"
        )

    recall_at_1 = sum(
        item["recall_at_1"] for item in results
    ) / len(results)

    recall_at_3 = sum(
        item["recall_at_3"] for item in results
    ) / len(results)

    recall_at_5 = sum(
        item["recall_at_5"] for item in results
    ) / len(results)

    avg_latency = sum(
        item["latency_seconds"] for item in results
    ) / len(results)

    print("\n" + "=" * 60)
    print("RAG EVALUATION")
    print("=" * 60)
    print(f"Questions: {len(results)}")
    print(f"Recall@1: {recall_at_1:.3f}")
    print(f"Recall@3: {recall_at_3:.3f}")
    print(f"Recall@5: {recall_at_5:.3f}")
    print(f"Average latency: {avg_latency:.3f}s")

    output_file = Path("eval/results.json")
    output_file.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nSaved: {output_file}")


if __name__ == "__main__":
    main()