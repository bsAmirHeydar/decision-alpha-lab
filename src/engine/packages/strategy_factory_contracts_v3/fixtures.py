"""Deterministic golden fixtures used by Python and MQL5 conformance tests."""
from __future__ import annotations
from .codec import CanonicalScaledInteger,canonical_json
from .enums import IdentityKind
from .identity import IdentityKey
from .time_model import KnownTimeChain,UtcInstant


def golden_identity_cases()->list[IdentityKey]:
    return [
        IdentityKey(IdentityKind.CONTEXT_OCCURRENCE,"exp0017.cycle_divergence","1.0.0","exp0017",{
            "confirmation_time_ms":1783800000000,
            "direction":"long",
            "primary_symbol":"US100",
            "reference_symbol":"US500",
            "source_event_id":"EXP0017_EVT_000042",
        }),
        IdentityKey(IdentityKind.COMPLETE_TREATMENT,"ucee.treatments","3.0.0","strategy_factory",{
            "entry_atom_id":"entry.stop.tight.v1",
            "exit_atom_id":"exit.fixed_rr.v1",
            "management_atom_id":"management.none.v1",
            "risk_atom_id":"risk.fixed_cash.v1",
            "stop_atom_id":"stop.structural.wide.v1",
        }),
        IdentityKey(IdentityKind.DATASET_ROW,"ucee.dataset","3.0.0","strategy_factory",{
            "context_occurrence_id":"uce3_context_occurrence_0000000000000000",
            "feature_schema_id":"alpha_lab.ucee/context_feature_vector@3.0.0",
            "label_contract_id":"net_r_after_costs.v1",
            "observation_cut_ms":1783800000000,
            "treatment_id":"uce3_complete_treatment_0000000000000000",
        }),
    ]


def golden_time_chain()->KnownTimeChain:
    return KnownTimeChain(
        UtcInstant(1783799940000,"market_event"),
        UtcInstant(1783800000000,"bar_close"),
        UtcInstant(1783800000000,"bar_close"),
        UtcInstant(1783800000000,"feature_cut"),
        UtcInstant(1783800000001,"decision"),
        UtcInstant(1783800000002,"execution"),
        UtcInstant(1783800000010,"broker"),
        UtcInstant(1783886400000,"label_engine"),
    )


def golden_codec_values()->list[object]:
    return [
        {"z":1,"a":"ASCII","escaped":"line\nquote\""},
        {"price":CanonicalScaledInteger(1234567,5),"negative_zero":CanonicalScaledInteger(0,4)},
        [None,True,False,-7,"é"],
    ]


def build_cross_language_vectors()->dict[str,object]:
    identities=golden_identity_cases()
    codecs=golden_codec_values()
    return {
        "contract_release":"3.0.0",
        "codec_vectors":[{"canonical_json":canonical_json(value),"input_index":i} for i,value in enumerate(codecs)],
        "identity_vectors":[{"canonical_material":item.canonical_material,"evidence_sha256":item.evidence_sha256,"stable_id":item.stable_id} for item in identities],
        "known_time_chain":golden_time_chain().material(),
    }
