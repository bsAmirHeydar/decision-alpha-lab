"""Executable UCE-I10 native conformance suite."""

from __future__ import annotations

from .audit import deterministic_replay_audit
from .canonical import canonical_sha256
from .catalog import CATALOG
from .compression import distill_linear, quantize_symmetric_int8
from .enums import MissingViewPolicy, QualificationDecision, TransferDecision
from .fusion import GatedFusion, LateWeightedFusion, StackedFusion
from .gates import evaluate_deep_admission
from .golden import candles, graph_case, graph_spec, qualification_evidence, raster_spec, sequence_case
from .graph import GraphMessagePassingModel, build_graph_artifact
from .qualification import qualify_deep_model
from .raster import RasterConvModel, audit_prefix_invariance, render_chart_raster
from .regime import CusumChangeDetector, DistanceNoveltyModel, RegimeExpertGate, RegimeModel
from .registry import DeepAlgorithmRegistry
from .sequence import CausalTemporalConvModel, validate_causal_sequence
from .transfer import evaluate_transfer_boundary


def run_conformance() -> dict:
    output: dict[str, object] = {"release": "UCE-I10", "version": "1.1.0"}

    sequence_values, sequence_targets, sequence_shape = sequence_case()
    sequence_a = CausalTemporalConvModel.fit(sequence_values, sequence_targets, sequence_shape)
    sequence_b = CausalTemporalConvModel.fit(sequence_values, sequence_targets, sequence_shape)
    sequence_predictions = [sequence_a.predict(row)[0] for row in sequence_values]
    validate_causal_sequence(
        sequence_values[0],
        sequence_shape,
        tuple(range(sequence_shape[0])),
        sequence_shape[0] - 1,
    )
    sequence_mae = sum(
        abs(target[0] - prediction)
        for target, prediction in zip(sequence_targets, sequence_predictions)
    ) / len(sequence_predictions)
    output["sequence"] = {
        "deterministic": sequence_a.state_hash == sequence_b.state_hash,
        "mae": sequence_mae,
        "state_hash": sequence_a.state_hash,
    }

    spec = raster_spec()
    candle_rows = candles()
    cut = candle_rows[19]["time_ms"]
    raster = render_chart_raster(spec, "ctx_golden", cut, candle_rows)
    future = (
        {
            "time_ms": cut + 60_000,
            "open": 500,
            "high": 600,
            "low": 400,
            "close": 550,
            "volume": 1,
        },
    )
    pixel_audit = audit_prefix_invariance(spec, "ctx_golden", cut, candle_rows, future)
    output["raster"] = {
        "shape": raster.shape,
        "prefix_invariant": pixel_audit.prefix_invariant,
        "changed_pixel_count": pixel_audit.changed_pixel_count,
        "hash": raster.evidence_hash,
    }

    raster_values = []
    raster_targets = []
    for index in range(24):
        artifact = render_chart_raster(
            spec,
            f"ctx_{index}",
            candle_rows[min(19 + index % 10, len(candle_rows) - 1)]["time_ms"],
            candle_rows,
        )
        raster_values.append(artifact.values)
        raster_targets.append((float(index % 5),))
    raster_model = RasterConvModel.fit(raster_values, raster_targets, raster.shape)
    output["vision"] = {
        "deterministic": raster_model.state_hash
        == RasterConvModel.fit(raster_values, raster_targets, raster.shape).state_hash,
        "prediction": raster_model.predict(raster_values[0])[0],
    }

    graph_values, graph_targets, node_count, feature_count, edges = graph_case()
    graph_definition = graph_spec()
    graph_artifact = build_graph_artifact(
        graph_definition,
        "ctx_graph",
        5_000,
        tuple(f"n{index}" for index in range(node_count)),
        tuple(1_000 + index for index in range(node_count)),
        tuple(
            tuple(graph_values[0][index * feature_count : (index + 1) * feature_count])
            for index in range(node_count)
        ),
        edges,
    )
    graph_model = GraphMessagePassingModel.fit(
        graph_values,
        graph_targets,
        node_count,
        feature_count,
        edges,
    )
    output["graph"] = {
        "topology_hash": graph_artifact.topology_hash,
        "deterministic": graph_model.state_hash
        == GraphMessagePassingModel.fit(
            graph_values,
            graph_targets,
            node_count,
            feature_count,
            edges,
        ).state_hash,
    }

    regime_rows = [
        (float(index % 7), float((index // 7) % 4), float(index % 2))
        for index in range(90)
    ]
    regime = RegimeModel.fit(regime_rows, 3)
    novelty = DistanceNoveltyModel.fit(regime_rows)
    change = CusumChangeDetector.fit([row[0] for row in regime_rows])
    gate = RegimeExpertGate(regime, novelty, ("e0", "e1", "e2"), 5, 0.3, 2.0)
    regime_prediction = gate.predict(
        "row0",
        regime_rows[0],
        change.score([row[0] for row in regime_rows[:20]]),
    )
    output["regime"] = {
        "support": regime.support,
        "decision": regime_prediction.decision.value,
        "deterministic": regime.state_hash == RegimeModel.fit(regime_rows, 3).state_hash,
    }

    fusion_targets = [0.7 * index + 0.3 * (index % 3) for index in range(40)]
    base_predictions = {
        "sequence": [value + 0.1 for value in fusion_targets],
        "graph": [value - 0.05 for value in fusion_targets],
    }
    late = LateWeightedFusion.fit(base_predictions, fusion_targets, MissingViewPolicy.GLOBAL_FALLBACK)
    stacked = StackedFusion.fit(base_predictions, fusion_targets)
    gated = GatedFusion.fit(base_predictions, fusion_targets)
    late_prediction = late.predict(
        "f0",
        {"sequence": base_predictions["sequence"][0], "graph": base_predictions["graph"][0]},
    )
    stacked_prediction = stacked.predict(
        "f0",
        {"sequence": base_predictions["sequence"][0], "graph": base_predictions["graph"][0]},
    )
    gated_prediction = gated.predict(
        "f0",
        {"sequence": base_predictions["sequence"][0], "graph": base_predictions["graph"][0]},
        {"sequence": 0.9, "graph": 0.8},
    )
    output["fusion"] = {
        "late_abstained": late_prediction.abstained,
        "stacked_value": stacked_prediction.value,
        "gated_abstained": gated_prediction.abstained,
        "weight_sum": sum(late_prediction.view_weights.values()),
    }

    student_features = [(float(index), float(index % 3)) for index in range(30)]
    teacher_predictions = [0.5 * index + 0.1 * (index % 3) for index in range(30)]
    coefficients, distillation = distill_linear(
        "teacher",
        "student",
        student_features,
        teacher_predictions,
        0.8,
        8.0,
        max_fidelity_mae=0.001,
    )
    _, _, quantization = quantize_symmetric_int8(coefficients, max_error=0.05)
    output["compression"] = {
        "distillation": distillation.accepted,
        "quantization": quantization.accepted,
        "ratio": distillation.compression_ratio,
    }

    transfer = evaluate_transfer_boundary(
        "source_manifest",
        "target_manifest",
        ("s1", "s2"),
        ("t1", "t2"),
        ("z1",),
        True,
    )
    output["transfer"] = {
        "decision": transfer.decision.value,
        "blockers": transfer.blockers,
    }

    admission = evaluate_deep_admission(
        "ds",
        "manifest",
        1_200,
        120,
        5,
        True,
        True,
        True,
        True,
        0.61,
        "aug_hash",
        "ablation_hash",
    )
    seeds, ablations, export = qualification_evidence()
    qualification = qualify_deep_model(
        "causal_temporal_conv_ridge@1.0.0",
        "manifest",
        admission,
        seeds,
        ablations,
        export,
        0.60,
        0.01,
        0.2,
        0.05,
        5.0,
    )
    output["qualification"] = {
        "admission": admission.decision.value,
        "decision": qualification.decision.value,
        "blockers": qualification.blockers,
    }

    snapshot = DeepAlgorithmRegistry().freeze().snapshot()
    replay = deterministic_replay_audit(lambda: DeepAlgorithmRegistry().freeze().snapshot())
    output["registry"] = {
        "count": len(snapshot.descriptors),
        "families": sorted({descriptor.family.value for descriptor in snapshot.descriptors}),
        "frozen": snapshot.frozen,
        "hash": snapshot.evidence_hash,
        "replay_passed": replay.passed,
    }

    output["passed"] = all(
        (
            output["sequence"]["deterministic"],
            output["sequence"]["mae"] < 0.05,
            output["raster"]["prefix_invariant"],
            output["vision"]["deterministic"],
            output["graph"]["deterministic"],
            output["regime"]["deterministic"],
            not output["fusion"]["late_abstained"],
            not output["fusion"]["gated_abstained"],
            abs(output["fusion"]["weight_sum"] - 1.0) < 1e-9,
            output["compression"]["distillation"],
            output["compression"]["quantization"],
            transfer.decision is TransferDecision.ACCEPT,
            qualification.decision is QualificationDecision.PROMOTABLE,
            len(CATALOG) == 17,
            snapshot.frozen,
            replay.passed,
        )
    )
    output["evidence_hash"] = canonical_sha256(output)
    return output
