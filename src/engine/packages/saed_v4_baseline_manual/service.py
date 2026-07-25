from __future__ import annotations
from .validation import validate_upstream
from .compiler import compile_program
from .interpreter import evaluate_program
from .baseline import build_registry
from .benchmark import evaluate_registry
from .exposure import build_exposure
from .corpus import build_pretraining_corpus_manifest
from .telemetry import build_telemetry
from .integrity import build_receipt
from .handoff import build_v4_11_handoff
from .claims import claim_ledger

def build_bundle(view_package,hypergraph,lattice,twin,program_sources):
    validate_upstream(view_package,lattice,twin)
    programs=[compile_program(x,view_package,lattice) for x in program_sources]
    traces=[evaluate_program(x,view_package) for x in programs]
    registry=build_registry(lattice,programs,traces)
    benchmark=evaluate_registry(registry,twin)
    exposure=build_exposure(registry,benchmark)
    corpus=build_pretraining_corpus_manifest(view_package,hypergraph,lattice)
    telemetry=build_telemetry(registry,benchmark,exposure,corpus)
    receipt=build_receipt(*programs,*traces,registry,benchmark,exposure,corpus,telemetry)
    handoff=build_v4_11_handoff(registry,benchmark,corpus,receipt)
    return {"compiled_programs":programs,"decision_traces":traces,"baseline_registry":registry,"benchmark":benchmark,"exposure_ledger":exposure,"corpus_manifest":corpus,"telemetry":telemetry,"integrity_receipt":receipt,"handoff":handoff,"claim_ledger":claim_ledger()}
