"""Build pseudo product pairs for schema and smoke tests."""

from __future__ import annotations

import csv
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def main() -> None:
    random.seed(7)
    OUT.mkdir(exist_ok=True)
    path = OUT / "product_pairs.csv"
    fields = [
        "pair_id",
        "product_id_a",
        "product_id_b",
        "title_a",
        "title_b",
        "image_path_a",
        "image_path_b",
        "category_path",
        "brand_token",
        "sku_attrs_a",
        "sku_attrs_b",
        "ocr_text_a",
        "ocr_text_b",
        "label_match",
        "negative_type",
    ]
    categories = ["apparel/tshirt", "3c/accessory", "home/storage", "beauty/skincare"]
    neg_types = ["random", "same_category_diff_style", "same_image_sku_conflict", "title_sim_image_diff", "ocr_marketing_noise"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for i in range(80):
            neg = random.choice(neg_types)
            label = int(neg == "random" and random.random() < 0.35)
            writer.writerow(
                {
                    "pair_id": f"pair_{i:04d}",
                    "product_id_a": f"pa_{i:04d}",
                    "product_id_b": f"pb_{i:04d}",
                    "title_a": "anonymized product title A",
                    "title_b": "anonymized product title B",
                    "image_path_a": f"images/a_{i:04d}.jpg",
                    "image_path_b": f"images/b_{i:04d}.jpg",
                    "category_path": random.choice(categories),
                    "brand_token": f"brand_{random.randint(1, 20):02d}",
                    "sku_attrs_a": "color=white;size=M;bundle=1",
                    "sku_attrs_b": "color=beige;size=M;bundle=1" if "sku" in neg else "color=white;size=M;bundle=1",
                    "ocr_text_a": "new arrival discount",
                    "ocr_text_b": "new arrival discount" if "ocr" in neg else "",
                    "label_match": label,
                    "negative_type": neg,
                }
            )
    print(f"wrote {path}")


if __name__ == "__main__":
    main()

