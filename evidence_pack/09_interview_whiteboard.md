# Interview Whiteboard

```text
Product title + main image
  |
  v
Pseudo / offline evaluation pairs
positive pairs + random negatives + hard negatives
  |
  v
Text Encoder                 Image Encoder
title tokens                 image description / visual surrogate
brand / attrs                subject / OCR / category
  |                           |
  v                           v
title embedding               image embedding
          \                   /
           cosine similarity
                   |
                   v
TopK Retrieval + threshold table
                   |
                   v
Recall@10 / NDCG@10 / high-score false positives
                   |
                   v
SKU conflict / OCR noise / title generalization badcases
```

## How to narrate it

Start from the ecommerce false-positive problem: similar titles and similar images are not always the same product. Then explain dual-encoder retrieval, hard negatives, threshold review, and badcase buckets.
