.PHONY: data train eval test all

data:
	python3 scripts/build_pseudo_pairs.py

train:
	python3 scripts/train_clip_baseline.py

eval:
	python3 scripts/evaluate_retrieval.py

test:
	python3 -m pytest -q

all: data train eval test
