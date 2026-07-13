from pathlib import Path
from fp_i08_weekly.golden import load_vectors,verify_vector_shape
ROOT=Path(__file__).resolve().parents[1]
def test_golden_vector_shape(): assert verify_vector_shape(load_vectors(ROOT/'artifacts/FP_I08_GOLDEN_WW_VECTORS.v1.json'))
