from __future__ import annotations
from .contracts import ContextSpecification,TournamentTemplateSpec,CompiledTournamentTemplate
from .canonical import canonical_sha256,stable_id
STAGES=('data_cut','treatment_freeze','trainer_budget','search_budget','walk_forward','anti_overfit','prospective_paper','runtime_bundle','promotion_handoff')
def default_template(spec:ContextSpecification,seed:int=160016)->TournamentTemplateSpec:
    return TournamentTemplateSpec(stable_id('tournament-template',{'spec':spec.spec_hash,'seed':seed}),'1.0.0',spec.spec_hash,'causal-data-cut-v1','shared-treatment-freeze-v1','bounded-trainer-budget-v1','bounded-search-budget-v1','uce-i12-anti-overfit-v1','untouched-prospective-paper-v1','uce-i14-runtime-v1','uce-i12-promotion-v1',seed)
def compile_template(template:TournamentTemplateSpec)->CompiledTournamentTemplate:
    identities={stage:canonical_sha256({'template_hash':template.template_hash,'stage':stage,'seed':template.seed}) for stage in STAGES}
    return CompiledTournamentTemplate(stable_id('compiled-tournament',identities),'1.0.0',template.template_hash,STAGES,identities,final_test_sealed=True,fixture_not_alpha_proof=True)
