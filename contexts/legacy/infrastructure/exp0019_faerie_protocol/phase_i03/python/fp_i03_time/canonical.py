"""Reuse FP-I02 canonical identity without creating a competing identity kernel."""
from fp_i02_kernel.canonical import canonical_json, canonical_sha256, stable_id

__all__ = ["canonical_json", "canonical_sha256", "stable_id"]
