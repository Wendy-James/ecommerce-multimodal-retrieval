#!/usr/bin/env bash
set -euo pipefail

python3 scripts/build_pseudo_pairs.py
python3 scripts/train_clip_baseline.py
python3 scripts/evaluate_retrieval.py
python3 -m pytest -q
