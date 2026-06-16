# Run Commands

## Full smoke-test pipeline

```bash
make all
```

or:

```bash
./run.sh
```

The pipeline builds pseudo ecommerce product pairs, trains a lightweight CLIP-style dual encoder, evaluates Recall@10/NDCG@10, and writes metrics/badcase artifacts.

## Tests

```bash
pytest -q
```

## Important outputs

- `outputs/product_pairs.csv`
- `outputs/title_embeddings.npy`
- `outputs/image_embeddings.npy`
- `outputs/metrics.csv`
- `experiments.csv`
- `ablation.csv`
- `badcases.csv`
