"""Create deterministic toy retrieval metrics for documentation."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def main() -> None:
    if not (OUT / "model_meta.json").exists():
        raise SystemExit("Run scripts/train_clip_baseline.py first.")
    rows = [
        {
            "metric": "Recall@10",
            "value": "0.663",
            "note": "toy metric mirrors experiment table field",
        },
        {
            "metric": "NDCG@10",
            "value": "0.549",
            "note": "toy metric mirrors experiment table field",
        },
        {
            "metric": "review_focus",
            "value": "sku_conflict,ocr_noise,title_generalization",
            "note": "badcase buckets for manual review",
        },
    ]
    path = OUT / "metrics.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()

