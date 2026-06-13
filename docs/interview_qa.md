# Interview Q&A

Safe positioning: this is an offline ecommerce multimodal retrieval evidence-chain project. It demonstrates image-text matching, hard-negative construction, threshold review, and badcase analysis. It is not a full online search/recommendation ownership claim.

## 1. What business problem does this solve?

In ecommerce search and product understanding, title-similar or image-similar products can still be wrong matches when SKU attributes conflict. For example, two shirts may look similar but differ in color, size, bundle count, or model number. A pure similarity score can create high-score false positives, so the project focuses on retrieval quality plus badcase buckets.

## 2. What is the CLIP-style baseline?

The baseline follows a dual-encoder structure:

- Image encoder: ViT-B-32-style visual encoder.
- Text encoder: transformer-style title/OCR/category encoder.
- Matching score: cosine similarity or inner product between normalized embeddings.
- Retrieval: top-k nearest product candidates.

The public repo uses pseudo data and deterministic scripts to show the workflow. In an interview, I should describe it as Chinese-CLIP/OpenCLIP-style reproduction, not as training a huge multimodal foundation model.

## 3. How is the contrastive loss written?

For a batch of matched image-text pairs, image embeddings and text embeddings are normalized. The similarity matrix is computed by image-text dot product divided by temperature. Cross entropy is applied in both directions:

- image-to-text classification
- text-to-image classification

This is often called InfoNCE-style contrastive learning. Hard negatives make the classification task harder because the wrong candidates are semantically close.

## 4. How are hard negatives constructed?

Hard negatives are sampled from the same or neighboring category when title or image similarity is high but SKU attributes conflict. Typical buckets:

- same category, different style
- similar main image, different color/size/model
- same marketing OCR phrase, different actual product
- similar title template, different SKU or bundle count

The key is to admit false-negative risk: some hard negatives may actually be substitutes. That is why I bucket and review them instead of claiming hard negatives always improve all metrics.

## 5. What metrics are used?

- `Recall@10`: whether the correct or accepted match is retrieved in top 10.
- `NDCG@10`: whether better candidates appear earlier.
- False-positive bucket review: checks high-score wrong matches by SKU conflict, OCR noise, title generalization, and cross-level category.
- Threshold table: helps choose score thresholds for manual review or downstream filtering.

## 6. Why can hard negatives reduce false positives but hurt recall?

Hard negatives force the model to separate similar but wrong products, so high-score false positives can decrease. However, if the negative set contains substitutes or mislabeled positives, the model may over-separate genuinely related products and hurt overall recall. This is why the repo records both Recall@10/NDCG@10 and badcase buckets.

## 7. What are the most important badcases?

| Bucket | Example | Reason |
|---|---|---|
| SKU attribute conflict | white vs beige shirt | Visual similarity is high but SKU attribute differs |
| Marketing OCR noise | "buy one get one" text | Promo text dominates embedding similarity |
| Title generalization | "new summer fashion" | Generic title lacks discriminative entity |
| Cross-level category | phone case for different models | Coarse category path hides model-number conflict |

## 8. What is the real deliverable?

The deliverable is a reproducible offline evaluation package: pseudo pair builder, CLIP-style baseline script, retrieval evaluation script, metrics CSV, badcase table, threshold/bucket notes, and interview explanation. It supports later product matching or similar-retrieval strategy evaluation, but I should not claim online ownership.
