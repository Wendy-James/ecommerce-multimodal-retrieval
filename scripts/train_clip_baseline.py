"""Train a lightweight CLIP-style dual encoder on pseudo product records.

This script builds vocabulary and character n-gram features from public pseudo
fields, trains two linear towers with an InfoNCE-style in-batch contrastive
loss, and exports normalized embeddings for retrieval evaluation.

When PyTorch is available, the same objective runs with torch modules. In
minimal CPU environments, a NumPy implementation keeps `make all` runnable.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

try:
    import torch
    from torch import nn
except Exception:  # pragma: no cover
    torch = None
    nn = None


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
INPUT_DIM = 96
EMBED_DIM = 32
EPOCHS = 120
LR = 0.12
SEED = 2026


def _tokens(text: str) -> list[str]:
    normalized = text.replace(";", " ").replace("=", " ").replace("/", " ").replace("_", " ")
    words = [token.lower() for token in normalized.split() if token.strip()]
    char_grams: list[str] = []
    compact = "".join(words)
    for n in (2, 3):
        char_grams.extend([f"char{n}:{compact[i:i+n]}" for i in range(max(0, len(compact) - n + 1))])
    return words + char_grams


def _build_vocab(texts: list[str], dim: int = INPUT_DIM) -> dict[str, int]:
    counts: dict[str, int] = {}
    for text in texts:
        for token in _tokens(text):
            counts[token] = counts.get(token, 0) + 1
    most_common = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:dim]
    return {token: idx for idx, (token, _) in enumerate(most_common)}


def _vectorize(text: str, vocab: dict[str, int], dim: int = INPUT_DIM) -> np.ndarray:
    vec = np.zeros(dim, dtype="float32")
    for token in _tokens(text):
        idx = vocab.get(token)
        if idx is not None:
            vec[idx] += 1.0
    return vec / (np.linalg.norm(vec) + 1e-8)


def _load_products() -> tuple[list[str], np.ndarray, np.ndarray]:
    path = OUT / "product_pairs.csv"
    if not path.exists():
        raise SystemExit("Run scripts/build_pseudo_pairs.py first.")
    products: dict[str, tuple[str, str]] = {}
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            products[row["product_id_a"]] = (
                " ".join([row["title_a"], row["category_path"], row["brand_token"], row["sku_attrs_a"], row["ocr_text_a"]]),
                " ".join([row["image_path_a"], row["category_path"], row["sku_attrs_a"], row["ocr_text_a"]]),
            )
            products[row["product_id_b"]] = (
                " ".join([row["title_b"], row["category_path"], row["brand_token"], row["sku_attrs_b"], row["ocr_text_b"]]),
                " ".join([row["image_path_b"], row["category_path"], row["sku_attrs_b"], row["ocr_text_b"]]),
            )
    ids = sorted(products)
    all_texts = [field for pid in ids for field in products[pid]]
    vocab = _build_vocab(all_texts)
    text_x = np.vstack([_vectorize(products[pid][0], vocab) for pid in ids])
    image_x = np.vstack([_vectorize(products[pid][1], vocab) for pid in ids])
    return ids, text_x, image_x


def _softmax(x: np.ndarray) -> np.ndarray:
    x = x - x.max(axis=1, keepdims=True)
    exp = np.exp(x)
    return exp / (exp.sum(axis=1, keepdims=True) + 1e-8)


def _train_numpy(text_x: np.ndarray, image_x: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[float]]:
    rng = np.random.default_rng(SEED)
    wt = rng.normal(0, 0.08, size=(INPUT_DIM, EMBED_DIM)).astype("float32")
    wi = rng.normal(0, 0.08, size=(INPUT_DIM, EMBED_DIM)).astype("float32")
    labels = np.arange(text_x.shape[0])
    losses: list[float] = []
    for _ in range(EPOCHS):
        text_z = text_x @ wt
        image_z = image_x @ wi
        text_z /= np.linalg.norm(text_z, axis=1, keepdims=True) + 1e-8
        image_z /= np.linalg.norm(image_z, axis=1, keepdims=True) + 1e-8
        logits = text_z @ image_z.T / 0.07
        probs = _softmax(logits)
        loss = -np.log(probs[np.arange(len(labels)), labels] + 1e-8).mean()
        losses.append(float(loss))
        grad_logits = probs
        grad_logits[np.arange(len(labels)), labels] -= 1.0
        grad_logits /= len(labels) * 0.07
        grad_t = grad_logits @ image_z
        grad_i = grad_logits.T @ text_z
        wt -= LR * (text_x.T @ grad_t)
        wi -= LR * (image_x.T @ grad_i)
    text_emb = text_x @ wt
    image_emb = image_x @ wi
    text_emb /= np.linalg.norm(text_emb, axis=1, keepdims=True) + 1e-8
    image_emb /= np.linalg.norm(image_emb, axis=1, keepdims=True) + 1e-8
    return text_emb.astype("float32"), image_emb.astype("float32"), losses


def _train_torch(text_x: np.ndarray, image_x: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[float]]:
    assert torch is not None and nn is not None
    torch.manual_seed(SEED)
    text = torch.tensor(text_x, dtype=torch.float32)
    image = torch.tensor(image_x, dtype=torch.float32)
    text_tower = nn.Linear(INPUT_DIM, EMBED_DIM, bias=False)
    image_tower = nn.Linear(INPUT_DIM, EMBED_DIM, bias=False)
    optim = torch.optim.Adam(list(text_tower.parameters()) + list(image_tower.parameters()), lr=0.03)
    labels = torch.arange(text.shape[0], dtype=torch.long)
    losses: list[float] = []
    for _ in range(EPOCHS):
        optim.zero_grad()
        text_z = nn.functional.normalize(text_tower(text), dim=1)
        image_z = nn.functional.normalize(image_tower(image), dim=1)
        logits = text_z @ image_z.T / 0.07
        loss = (nn.functional.cross_entropy(logits, labels) + nn.functional.cross_entropy(logits.T, labels)) / 2
        loss.backward()
        optim.step()
        losses.append(float(loss.detach().cpu()))
    text_emb = nn.functional.normalize(text_tower(text), dim=1).detach().cpu().numpy()
    image_emb = nn.functional.normalize(image_tower(image), dim=1).detach().cpu().numpy()
    return text_emb.astype("float32"), image_emb.astype("float32"), losses


def main() -> None:
    product_ids, text_x, image_x = _load_products()
    if torch is not None:
        text_emb, image_emb, losses = _train_torch(text_x, image_x)
        backend = "pytorch"
    else:
        text_emb, image_emb, losses = _train_numpy(text_x, image_x)
        backend = "numpy_infonce"

    np.save(OUT / "title_embeddings.npy", text_emb)
    np.save(OUT / "image_embeddings.npy", image_emb)
    (OUT / "product_id_map.json").write_text(json.dumps({pid: i for i, pid in enumerate(product_ids)}, indent=2), encoding="utf-8")
    meta = {
        "model": "clip_style_dual_encoder",
        "backend": backend,
        "loss": "InfoNCE cross entropy with in-batch negatives",
        "feature_encoder": "vocabulary_and_character_ngram_vectorizer",
        "input_dim": INPUT_DIM,
        "embedding_dim": EMBED_DIM,
        "num_products": len(product_ids),
        "final_loss": round(losses[-1], 6),
    }
    (OUT / "model_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    preview = {
        "product_id": product_ids[0],
        "title_embedding_head": [round(float(x), 6) for x in text_emb[0, :6]],
        "image_embedding_head": [round(float(x), 6) for x in image_emb[0, :6]],
    }
    (OUT / "embeddings_preview.json").write_text(json.dumps(preview, indent=2), encoding="utf-8")
    print(f"trained {meta['model']} with {backend}; final_loss={meta['final_loss']}")
    print(f"wrote {OUT / 'model_meta.json'}")


if __name__ == "__main__":
    main()
