"""Evaluate trained CLIP-style embeddings on pseudo product-pair labels."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def _ndcg_at_k(labels: list[int], k: int) -> float:
    hits = labels[:k]
    dcg = sum(y / math.log2(i + 2) for i, y in enumerate(hits))
    ideal = sorted(labels, reverse=True)[:k]
    idcg = sum(y / math.log2(i + 2) for i, y in enumerate(ideal))
    return dcg / (idcg + 1e-8)


def main() -> None:
    required = [OUT / "title_embeddings.npy", OUT / "image_embeddings.npy", OUT / "product_id_map.json", OUT / "product_pairs.csv"]
    if not all(path.exists() for path in required):
        raise SystemExit("Run scripts/build_pseudo_pairs.py and scripts/train_clip_baseline.py first.")

    title_emb = np.load(OUT / "title_embeddings.npy")
    image_emb = np.load(OUT / "image_embeddings.npy")
    product2idx = json.loads((OUT / "product_id_map.json").read_text(encoding="utf-8"))
    sim = title_emb @ image_emb.T
    k = min(10, sim.shape[1])
    hit_flags: list[int] = []
    ndcgs: list[float] = []
    for i in range(sim.shape[0]):
        ranked = list(np.argsort(-sim[i]))
        labels = [1 if idx == i else 0 for idx in ranked]
        hit_flags.append(int(i in ranked[:k]))
        ndcgs.append(_ndcg_at_k(labels, k))

    scored_rows = []
    with (OUT / "product_pairs.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ia = product2idx[row["product_id_a"]]
            ib = product2idx[row["product_id_b"]]
            domain_bonus = 0.10 if row["sku_attrs_a"] == row["sku_attrs_b"] else -0.05
            score = float((title_emb[ia] @ image_emb[ib] + title_emb[ib] @ image_emb[ia]) / 2 + domain_bonus)
            scored_rows.append({**row, "score": score, "label": int(row["label_match"])})

    ranked = sorted(scored_rows, key=lambda r: r["score"], reverse=True)
    focus = sorted({row["negative_type"] for row in ranked[:20] if row["label"] == 0})

    rows = [
        {"metric": "Recall@10", "value": f"{np.mean(hit_flags):.3f}", "note": "title-to-image retrieval from trained dual-encoder embeddings"},
        {"metric": "NDCG@10", "value": f"{np.mean(ndcgs):.3f}", "note": "title-to-image retrieval from trained dual-encoder embeddings"},
        {"metric": "review_focus", "value": ",".join(focus), "note": "top-score false-positive buckets for manual review"},
    ]
    path = OUT / "metrics.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "scored_pairs.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["pair_id", "product_id_a", "product_id_b", "label_match", "negative_type", "score"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in ranked:
            writer.writerow({key: row[key] for key in fieldnames})
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
