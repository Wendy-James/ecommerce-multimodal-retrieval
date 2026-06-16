# E-commerce Multimodal Retrieval Evidence Pack

## Interview positioning

This repository supports the ecommerce image-text retrieval story in the resume. It is a sanitized public reproduction of an offline retrieval evaluation workflow, not original internship code or private merchant data.

## Problem

E-commerce similar-product retrieval can produce high-score false positives when titles are similar but SKU attributes conflict, or when main images look similar but products are not the same style/model/package.

## What I can explain

- How title-image pairs are represented in a CLIP-style dual encoder.
- Why hard negatives are necessary for high-score false positives.
- Why hard negatives can also introduce false negatives.
- How Recall@10 and NDCG@10 differ.
- How SKU conflict, OCR marketing words, title generalization, and same-category different-style badcases are reviewed.

## Main files

- `data_schema.md`: pseudo product pair fields and labels.
- `scripts/build_pseudo_pairs.py`: pseudo ecommerce pair generation.
- `scripts/train_clip_baseline.py`: lightweight trainable CLIP-style dual encoder.
- `scripts/evaluate_retrieval.py`: Recall@10 and NDCG@10 evaluation.
- `experiments.csv`: experiment metrics.
- `ablation.csv`: hard negative and threshold ablation.
- `badcases.csv`: SKU/OCR/title/category failure examples.
