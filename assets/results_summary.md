# Results Summary

Pseudo evidence table for the resume project:

| setup | Recall@10 | NDCG@10 | review focus |
|---|---:|---:|---|
| Chinese-CLIP baseline + random negatives | 0.641 | 0.522 | general retrieval |
| Chinese-CLIP + mixed hard negatives | 0.658 | 0.541 | SKU conflict |
| Dual encoder + lightweight rerank features | 0.663 | 0.549 | score bucket and badcase review |

The project should be discussed as an offline sample/manual-review-set workflow, not as ownership of a full online recommendation system.

