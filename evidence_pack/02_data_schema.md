# Data Schema

This public repository uses pseudo/anonymized ecommerce examples. It does not contain merchant data, product images, platform labels, or original internship code.

| Field | Meaning | Example use |
|---|---|---|
| `product_id` | anonymized product id | retrieval target |
| `title` | pseudo product title | text encoder input |
| `image_desc` | pseudo image description | image-side surrogate input |
| `category` | product category | bucketed evaluation |
| `brand_token` | anonymized brand token | false-positive bucket |
| `sku_attrs` | color/size/model/package attributes | SKU conflict detection |
| `ocr_tokens` | marketing/OCR tokens from image | OCR-noise analysis |
| `pair_label` | positive / random negative / hard negative | training and evaluation |
| `hard_negative_type` | same-category different-style, SKU conflict, OCR noise | badcase attribution |

## Label design

Positive pairs represent title-image pairs that should match or retrieve each other.

Hard negatives represent pairs that are visually/textually close but business-wise different, such as same category but different model, similar image with SKU conflict, or title template similarity with different product attributes.
