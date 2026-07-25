"""Teacher/student distillation and deterministic symmetric quantization."""

from __future__ import annotations

from typing import Sequence

from .canonical import canonical_sha256, stable_id
from .contracts import DistillationReport, QuantizationReport
from .errors import DeepViewError
from .math_utils import mae, ridge_fit, ridge_predict


def distill_linear(
    teacher_key: str,
    student_key: str,
    student_features: Sequence[Sequence[float]],
    teacher_predictions: Sequence[float],
    teacher_metric: float,
    compression_ratio: float,
    alpha: float = 1e-3,
    max_fidelity_mae: float = 0.05,
    evaluation_features: Sequence[Sequence[float]] | None = None,
    evaluation_teacher_predictions: Sequence[float] | None = None,
):
    if len(student_features) != len(teacher_predictions) or not student_features:
        raise DeepViewError("invalid_distillation_training_set", "distillation rows must be non-empty and aligned")
    if compression_ratio <= 1.0:
        raise DeepViewError("invalid_compression_ratio", "compression ratio must exceed one")
    coefficients = ridge_fit(student_features, teacher_predictions, alpha)
    eval_features = evaluation_features or student_features
    eval_teacher = evaluation_teacher_predictions or teacher_predictions
    if len(eval_features) != len(eval_teacher):
        raise DeepViewError("distillation_evaluation_mismatch", "evaluation rows and teacher predictions differ")
    predictions = [ridge_predict(coefficients, row) for row in eval_features]
    fidelity = mae(predictions, eval_teacher)
    student_metric = -fidelity
    accepted = fidelity <= max_fidelity_mae
    material = {
        "teacher_key": teacher_key,
        "student_key": student_key,
        "training_row_count": len(student_features),
        "evaluation_row_count": len(eval_features),
        "teacher_metric": float(teacher_metric),
        "student_metric": student_metric,
        "fidelity_mae": fidelity,
        "compression_ratio": float(compression_ratio),
        "accepted": accepted,
        "coefficients": coefficients,
    }
    report = DistillationReport(
        report_id=stable_id("ucedistill", material),
        teacher_key=teacher_key,
        student_key=student_key,
        row_count=len(eval_features),
        teacher_metric=float(teacher_metric),
        student_metric=student_metric,
        fidelity_mae=fidelity,
        compression_ratio=float(compression_ratio),
        accepted=accepted,
        limitations=(
            "Reference student is linear and must still pass downstream economic parity.",
            "Production acceptance requires held-out or OOF teacher predictions.",
        ),
        evidence_hash=canonical_sha256(material),
    )
    return coefficients, report


def quantize_symmetric_int8(values: Sequence[float], max_error: float = 0.02):
    if max_error < 0:
        raise DeepViewError("negative_quantization_error", "maximum quantization error cannot be negative")
    material_values = tuple(float(value) for value in values)
    maximum = max((abs(value) for value in material_values), default=0.0)
    scale = maximum / 127.0 if maximum else 1.0
    quantized = tuple(max(-127, min(127, int(round(value / scale)))) for value in material_values)
    dequantized = tuple(value * scale for value in quantized)
    errors = [abs(left - right) for left, right in zip(material_values, dequantized)]
    max_abs_error = max(errors, default=0.0)
    mean_abs_error = sum(errors) / len(errors) if errors else 0.0
    accepted = max_abs_error <= max_error
    material = {
        "bits": 8,
        "scale": scale,
        "zero_point": 0,
        "max_abs_error": max_abs_error,
        "mean_abs_error": mean_abs_error,
        "accepted": accepted,
        "quantized": quantized,
    }
    return quantized, scale, QuantizationReport(
        report_id=stable_id("ucequant", material),
        bits=8,
        scale=scale,
        zero_point=0,
        max_abs_error=max_abs_error,
        mean_abs_error=mean_abs_error,
        accepted=accepted,
        evidence_hash=canonical_sha256(material),
    )
