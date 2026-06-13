# Data Schema

Pseudo schema for e-commerce multimodal retrieval. All examples are anonymized.

## product_pairs.csv

| field | type | description |
|---|---:|---|
| pair_id | string | anonymized pair id |
| product_id_a | string | query product id |
| product_id_b | string | candidate product id |
| title_a | string | query product title |
| title_b | string | candidate product title |
| image_path_a | string | pseudo image path |
| image_path_b | string | pseudo image path |
| category_path | string | category hierarchy |
| brand_token | string | anonymized brand token |
| sku_attrs_a | string | normalized SKU attributes for product A |
| sku_attrs_b | string | normalized SKU attributes for product B |
| ocr_text_a | string | pseudo OCR text |
| ocr_text_b | string | pseudo OCR text |
| label_match | int | whether pair is accepted as matching/similar |
| negative_type | string | random, same_category, sku_conflict, title_sim_image_diff |

## hard negative types

- `same_category_diff_style`: same category but different style.
- `same_image_sku_conflict`: similar image but color, size, model, or bundle count conflicts.
- `title_sim_image_diff`: title is similar but product body differs.
- `ocr_marketing_noise`: marketing OCR text is similar but product is different.

## evaluation buckets

- Category path.
- OCR token ratio.
- Subject area ratio.
- Title length.
- Score range.
- SKU conflict type.

