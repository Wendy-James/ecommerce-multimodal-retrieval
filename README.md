# ecommerce-multimodal-retrieval

E-commerce image-text retrieval reproduction and evidence-chain repository for algorithm internship interviews. The project documents a credible offline workflow for product title-image matching, CLIP-style dual-encoder retrieval, hard negative construction, top-k evaluation, threshold analysis, and badcase review.

**This public repo is a sanitized reproduction of the workflow, not the original internship code or data.** The internship-side work used an internal offline review/evaluation protocol; this repository uses the same field design, retrieval chain, metric style, and badcase taxonomy with pseudo/anonymized samples so the method can be inspected publicly.

No private merchant, product, or platform data is included. The repository uses pseudo schemas and anonymized examples.

## Project Positioning

- Scenario: e-commerce product image-text matching / similar product retrieval.
- Core problem: high-score false positives caused by similar titles or similar main images but conflicting SKU attributes.
- Baseline: Chinese-CLIP / OpenCLIP style dual encoder.
- Retrieval: vector search with top-k evaluation.
- Metrics: Recall@10, NDCG@10, false-positive review, bucketed badcase analysis.

## Evidence Snapshot

![metrics snapshot](assets/metrics_snapshot.svg)

| Resume Claim | Repository Evidence |
|---|---|
| Product title-image matching / similar retrieval | `data_schema.md`, `scripts/build_pseudo_pairs.py`, `outputs/product_pairs.csv` |
| CLIP-style dual encoder baseline | `scripts/train_clip_baseline.py`, `outputs/model_meta.json`, `outputs/embeddings_preview.json` |
| Hard negative construction | `experiments.csv`, `ablation.csv`, `badcases.csv`, `docs/interview_qa.md` |
| SKU conflict and OCR noise review | `badcases.csv` with 10 anonymized failure buckets, `assets/results_summary.md` |
| Recall@10 / NDCG@10 evaluation | `experiments.csv`, `outputs/metrics.csv`, `scripts/evaluate_retrieval.py` |
| Interview-safe boundary | `docs/experiment_log.md`, `docs/interview_qa.md` |
| Public evidence boundary | `docs/dev_log.md`, `tests/` |

## Data Boundary

If asked whether the resume-side 8000 title-image pairs and this GitHub repo are the same dataset, the answer is:

> No. The resume describes the internship-side offline sample/review protocol, which cannot be published. This GitHub repository is a sanitized public reproduction of the same workflow: same schema style, same hard-negative logic, same Faiss-style retrieval evaluation, same metrics table format, and same SKU/OCR/title/category badcase taxonomy, but no internal merchant/product/platform data.

## Repository Structure

```text
.
├── README.md
├── data_schema.md
├── experiments.csv
├── ablation.csv
├── badcases.csv
├── Makefile
├── run.sh
├── requirements.txt
├── scripts/
│   ├── build_pseudo_pairs.py
│   ├── train_clip_baseline.py
│   └── evaluate_retrieval.py
├── tests/
│   ├── test_badcases.py
│   ├── test_metrics.py
│   └── test_pseudo_pairs.py
└── assets/
    └── results_summary.md
```

## Quick Start

Recommended:

```bash
make all
```

Equivalent manual commands:

```bash
python scripts/build_pseudo_pairs.py
python scripts/train_clip_baseline.py
python scripts/evaluate_retrieval.py
python -m pytest -q
```

The scripts create pseudo product pairs and deterministic toy metrics. They document the experiment evidence chain, not real production data.

## Interview Talking Points

1. Hard negatives are domain-specific: same category different style, same image different SKU, similar title but different product.
2. SKU conflicts matter: color, size, model number, bundle count, and variant attributes can create dangerous false positives.
3. Do not claim online ownership: this is an offline sample / manual review set used for threshold and badcase analysis.
4. Always discuss bucketed evaluation: category, OCR ratio, subject area, title length, and score range.

## What This Repo Does Not Claim

- It is not a full online product-search owner project.
- It does not contain merchant private data or real SKU catalogs.
- It does not claim online A/B lift.
- It is an offline evidence-chain repo for multimodal retrieval, threshold review, and badcase discussion.
