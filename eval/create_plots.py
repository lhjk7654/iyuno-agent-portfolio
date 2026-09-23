import json
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_FILE = BASE_DIR / "eval" / "metrics.json"
PLOTS_DIR = BASE_DIR / "eval" / "plots"

PLOTS_DIR.mkdir(parents=True, exist_ok=True)

with open(METRICS_FILE, "r", encoding="utf-8") as f:
    metrics = json.load(f)

# 1. Recall metrics
recall = metrics["retrieval"]

plt.figure(figsize=(8, 5))
labels = ["Recall@1", "Recall@3", "Recall@5"]
values = [
    recall["recall_at_1"],
    recall["recall_at_3"],
    recall["recall_at_5"]
]

plt.bar(labels, values)
plt.ylim(0, 1)
plt.ylabel("Recall")
plt.title("Retrieval Recall")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "recall_metrics.png", dpi=200)
plt.close()

# 2. Retrieval latency
plt.figure(figsize=(7, 5))
plt.bar(
    ["Average Retrieval Latency"],
    [recall["average_retrieval_latency_seconds"]]
)
plt.ylabel("Seconds")
plt.title("Average Retrieval Latency")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "latency.png", dpi=200)
plt.close()

# 3. Evaluation summary
faithfulness = metrics["faithfulness"]

plt.figure(figsize=(8, 5))
labels = ["Recall@1", "Recall@3", "Recall@5", "Faithfulness\n(5-sample)"]
values = [
    recall["recall_at_1"],
    recall["recall_at_3"],
    recall["recall_at_5"],
    faithfulness["score"]
]

plt.bar(labels, values)
plt.ylim(0, 1)
plt.ylabel("Score")
plt.title("Evaluation Summary")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "evaluation_summary.png", dpi=200)
plt.close()

print("Evaluation plots created:")
print(PLOTS_DIR / "recall_metrics.png")
print(PLOTS_DIR / "latency.png")
print(PLOTS_DIR / "evaluation_summary.png")
