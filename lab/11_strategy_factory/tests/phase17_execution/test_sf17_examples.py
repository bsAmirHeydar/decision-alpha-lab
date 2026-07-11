import json
from pathlib import Path

def test_examples_parse():
    root=Path(__file__).resolve().parents[2]/"examples"/"phase17"
    for p in root.glob("*.json"): json.loads(p.read_text())
