# Roadmap

This repository is maintained as a public reproduction of an e-commerce image-text retrieval workflow. The emphasis is on domain-specific error analysis: SKU conflict, OCR noise, title generalization, and visually similar but semantically different products.

## Near-term

- Add a threshold sweep table for score buckets and review precision.
- Expand hard-negative buckets for same-category different-style, same-title different-SKU, and OCR-heavy product cards.
- Add a lightweight reranking baseline using text attributes and visual score features.

## Evaluation

- Keep Recall@10 and NDCG@10 as the top-k retrieval metrics.
- Track high-score false positives separately from general recall.
- Add category-level and OCR-ratio buckets to make failure patterns easier to inspect.

## Engineering

- Keep `make all` CPU-friendly and deterministic.
- Keep badcase examples anonymized and schema-compatible.
- Prefer small updates that change one experiment table, one script, or one badcase taxonomy at a time.
