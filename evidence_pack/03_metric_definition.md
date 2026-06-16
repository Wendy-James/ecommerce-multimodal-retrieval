# Metric Definition

## Recall@10

Checks whether the expected matching product appears in the top 10 retrieved candidates.

Use case: first-stage retrieval coverage.

## NDCG@10

Adds rank position sensitivity. A correct match at rank 1 is better than the same match at rank 10.

Use case: evaluates whether the retrieval list is not only broad but also ordered well.

## High-score false positive review

For ecommerce retrieval, a high cosine score is not enough. The review focuses on:

- SKU conflict;
- same-category different style;
- OCR marketing noise;
- title template generalization;
- similar main image but different product identity.

## Threshold table

The threshold-metric table records how different score thresholds affect recall, precision proxy, high-score false positives, and manual review workload.
