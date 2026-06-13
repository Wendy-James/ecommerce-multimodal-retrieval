"""Toy CLIP-style dual encoder placeholder.

The script exports deterministic pseudo embeddings for product titles and images
so the repository has a runnable evidence chain without private product data.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def vec(key: str, dim: int = 32) -> list[float]:
    seed = int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "little")
    rng = np.random.default_rng(seed)
    x = rng.normal(size=dim)
    x = x / (np.linalg.norm(x) + 1e-8)
    return x.round(6).tolist()


def main() -> None:
    path = OUT / "product_pairs.csv"
    if not path.exists():
        raise SystemExit("Run scripts/build_pseudo_pairs.py first.")
    embeddings = {}
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            embeddings[row["product_id_a"]] = {
                "title_embedding": vec(row["title_a"] + row["product_id_a"]),
                "image_embedding": vec(row["image_path_a"]),
            }
            embeddings[row["product_id_b"]] = {
                "title_embedding": vec(row["title_b"] + row["product_id_b"]),
                "image_embedding": vec(row["image_path_b"]),
            }
    meta = {
        "model": "toy_chinese_clip_openclip_dual_encoder",
        "loss": "InfoNCE / cross entropy with in-batch negatives",
        "embedding_dim": 32,
        "num_products": len(embeddings),
    }
    (OUT / "model_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (OUT / "embeddings_preview.json").write_text(json.dumps(embeddings)[:2000], encoding="utf-8")
    print(f"wrote {OUT / 'model_meta.json'}")


if __name__ == "__main__":
    main()

