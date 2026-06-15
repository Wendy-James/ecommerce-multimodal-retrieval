from __future__ import annotations

import csv
from pathlib import Path

from scripts import build_pseudo_pairs


ROOT = Path(__file__).resolve().parents[1]


def test_pseudo_pairs_include_schema_and_labels() -> None:
    build_pseudo_pairs.main()
    rows = list(csv.DictReader((ROOT / "outputs" / "product_pairs.csv").open(encoding="utf-8")))

    assert rows
    required = {"pair_id", "product_id_a", "product_id_b", "category_path", "sku_attrs_a", "sku_attrs_b", "label_match", "negative_type"}
    assert required.issubset(rows[0])
    assert {row["label_match"] for row in rows}.issubset({"0", "1"})


def test_hard_negative_buckets_are_present() -> None:
    rows = list(csv.DictReader((ROOT / "outputs" / "product_pairs.csv").open(encoding="utf-8")))
    negative_types = {row["negative_type"] for row in rows}

    assert "same_image_sku_conflict" in negative_types
    assert "ocr_marketing_noise" in negative_types
    assert "same_category_diff_style" in negative_types
