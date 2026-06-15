from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_badcase_table_covers_ecommerce_error_buckets() -> None:
    rows = list(csv.DictReader((ROOT / "badcases.csv").open(encoding="utf-8")))
    error_types = {row["error_type"] for row in rows}

    assert len(rows) >= 10
    assert "sku_attribute_conflict" in error_types
    assert "marketing_ocr_noise" in error_types
    assert "title_generalization" in error_types
    assert "cross_level_category" in error_types


def test_sku_conflict_badcase_has_review_action() -> None:
    rows = list(csv.DictReader((ROOT / "badcases.csv").open(encoding="utf-8")))
    sku_case = next(row for row in rows if row["error_type"] == "sku_attribute_conflict")

    assert sku_case["sku_conflict"]
    assert "hard negative" in sku_case["next_action"]
