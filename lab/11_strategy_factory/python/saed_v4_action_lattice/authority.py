from __future__ import annotations

def authority_boundary() -> dict[str, bool]:
    return {
        'read_frozen_treatment_dsl': True,
        'read_semantic_temporal_hypergraph': True,
        'enumerate_bounded_candidates': True,
        'evaluate_structural_constraints': True,
        'build_action_lattice': True,
        'emit_v4_08_handoff': True,
        'mutate_treatment_dsl': False,
        'generate_unbounded_actions': False,
        'use_future_outcomes': False,
        'rank_by_realized_outcome': False,
        'select_treatment': False,
        'train_model': False,
        'allocate_risk': False,
        'activate_runtime': False,
        'send_order': False,
        'network_access': False,
    }

def assert_safe_authority(authority: dict[str,bool]) -> None:
    prohibited=('mutate_treatment_dsl','generate_unbounded_actions','use_future_outcomes','rank_by_realized_outcome','select_treatment','train_model','allocate_risk','activate_runtime','send_order','network_access')
    enabled=[k for k in prohibited if authority.get(k)]
    if enabled: raise ValueError('prohibited authority enabled: '+','.join(enabled))
