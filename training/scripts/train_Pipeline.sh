#!/usr/bin/env bash
set -euo pipefail

echo "⏳ Pulling new data…"
bash scripts/update_data.sh

echo "🧹 Preprocessing…"
python training/data_processing.py --input data/raw.csv --output data/clean.csv

echo "🏋️ Training…"
python training/training_scripts.py --config config/train.yaml

echo "📊 Evaluating…"
python training/model_evaluation.py --equity equity_curve.csv

echo "✅ Done!"
