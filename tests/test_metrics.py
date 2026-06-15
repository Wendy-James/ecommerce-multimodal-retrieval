from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_experiment_metrics_track_recall_and_ndcg() -> None:
    rows = list(csv.DictReader((ROOT / "experiments.csv").open(encoding="utf-8")))
    baseline = next(row for row in rows if row["run_id"] == "emr_001")
    best = next(row for row in rows if row["run_id"] == "emr_004")

    assert float(best["recall_at_10"]) > float(baseline["recall_at_10"])
    assert float(best["ndcg_at_10"]) > float(baseline["ndcg_at_10"])
    assert best["negative_type"] == "mixed_hard_negative"


def test_outputs_metrics_use_same_public_fields() -> None:
    rows = list(csv.DictReader((ROOT / "outputs" / "metrics.csv").open(encoding="utf-8")))
    metrics = {row["metric"]: row["value"] for row in rows}

    assert metrics["Recall@10"] == "0.663"
    assert metrics["NDCG@10"] == "0.549"
    assert "sku_conflict" in metrics["review_focus"]
