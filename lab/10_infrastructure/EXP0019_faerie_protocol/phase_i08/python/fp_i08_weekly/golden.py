import json
from pathlib import Path
def load_vectors(path): return json.loads(Path(path).read_text())
def verify_vector_shape(data):
    required={"vector_version","cases"};return required.issubset(data) and all({"case_id","purpose","expected"}.issubset(c) for c in data["cases"])
