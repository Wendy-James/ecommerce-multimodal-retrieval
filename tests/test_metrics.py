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

    assert 0.0 <= float(metrics["Recall@10"]) <= 1.0
    assert 0.0 <= float(metrics["NDCG@10"]) <= 1.0
    assert float(metrics["Recall@10"]) > 0.0
    assert metrics["review_focus"]


def test_training_output_is_not_placeholder() -> None:
    import json

    meta = json.loads((ROOT / "outputs" / "model_meta.json").read_text(encoding="utf-8"))

    assert meta["model"] == "clip_style_dual_encoder"
    assert meta["backend"] in {"numpy_infonce", "pytorch"}
    assert meta["final_loss"] > 0
    assert (ROOT / "outputs" / "title_embeddings.npy").exists()
    assert (ROOT / "outputs" / "image_embeddings.npy").exists()
