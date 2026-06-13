# Experiment Log

## Goal

Build a defensible ecommerce multimodal retrieval reproduction for algorithm-intern interviews. The project should explain:

- Why product image-text matching is a real ecommerce problem.
- Why CLIP-style dual encoders are a reasonable baseline.
- Why hard negatives need ecommerce-specific buckets.
- Why metrics must be paired with badcase analysis.

## Experiment Summary

| Run | Change | Recall@10 | NDCG@10 | Main bucket | Decision |
|---|---|---:|---:|---|---|
| `emr_001` | Chinese-CLIP-style baseline with random negatives | 0.641 | 0.522 | General | Keep as baseline |
| `emr_002` | Add mixed hard negatives | 0.658 | 0.541 | SKU conflict | Keep, improves difficult false-positive buckets |
| `emr_003` | OpenCLIP-style feature probe | 0.652 | 0.536 | OCR marketing noise | Keep as model comparison |
| `emr_004` | Add lightweight rerank features | 0.663 | 0.549 | Score bucket | Main result for evidence chain |

## Why The Improvement Is Credible

The improvement is modest, which is more believable for an offline reproduction. The project does not claim a large online business lift. The key contribution is not only Recall@10 movement, but also the structured analysis of high-score false positives:

- SKU conflict: color, size, model number, bundle count.
- OCR marketing noise: promotion words dominate similarity.
- Title generalization: generic titles hide product differences.
- Cross-level category: coarse category labels confuse similar shapes.

## Threshold Review

| Score range | Review action | Risk |
|---|---|---|
| `>= 0.85` | Manual review high-score false positives | SKU conflict and model mismatch |
| `0.70 - 0.85` | Use category and attribute checks before accepting | OCR and generic-title noise |
| `< 0.70` | Usually not accepted as similar item | Recall loss for sparse descriptions |

## Safe Resume Wording

Use:

> Built an offline ecommerce image-text retrieval reproduction with CLIP-style dual encoder, hard-negative construction, Recall@10/NDCG@10 evaluation, threshold review, and SKU/OCR/title badcase analysis.

Avoid:

> Owned the full ecommerce retrieval system, used private merchant data, or improved online GMV/CTR.
