# Development Log

## Public Evidence Boundary

This repository is a public evidence repo organized in **June 2026** for resume and interview review. The public commit history should not be described as the full original learning timeline.

This public repo is a sanitized reproduction of the workflow, not the original internship code or data. The internship-side offline review/evaluation set cannot be published; this repo keeps the schema style, retrieval chain, metrics, and badcase taxonomy with pseudo/anonymized samples.

The public version contains:

- pseudo/anonymized ecommerce product pairs
- CLIP-style baseline scripts
- retrieval evaluation outputs
- experiment CSV and badcase table
- interview notes and pytest smoke tests

The public version does not contain:

- merchant private data
- real SKU catalog data
- online retrieval service code
- A/B-test or GMV/CTR ownership claims

## Why The Repo Was Organized This Way

The resume mentions ecommerce image-text retrieval and similar-product matching. To make the claim inspectable, this repo exposes:

1. pseudo product-pair schema
2. CLIP-style dual-encoder training entry point
3. retrieval evaluation script
4. Recall@10/NDCG@10 experiment table
5. SKU/OCR/title/category badcase records
6. tests and one-command execution

## Reproducible Commands

```bash
make all
```

or:

```bash
./run.sh
```

## Interview Wording

Safe wording:

> I organized a public evidence version in June 2026. It uses pseudo ecommerce product pairs to reproduce the image-text retrieval workflow and make hard-negative construction, metrics, and badcases inspectable.

If asked whether the public GitHub data is the same as the resume-side internship sample:

> No. The resume describes the internship-side offline evaluation protocol. GitHub is a sanitized public reproduction of the same field design and evaluation method, without internal merchant/product/platform data.

Avoid:

> This repo is a full production owner project or contains real merchant data.
