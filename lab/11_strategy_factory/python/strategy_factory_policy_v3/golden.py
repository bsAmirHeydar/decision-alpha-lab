from __future__ import annotations
from .contracts import *
from .enums import *
from .fallback import default_fallback_policy
from .authority import default_authority_matrix

def h(ch='a'): return ch*64
def golden_admission(): return PromotionAdmission('admit:model-alpha','1.0.0',h('a'),h('b'),True,'promote','model-alpha','1.2.0',('ctx.breakout',),('market','limit'),('low','standard'),('enter_long','no_action'),1000,999999,('filter','rank','treatment','risk'),('synthetic_fixture',))
def golden_manual(): return ManualPolicyDefinition('setup.breakout','1.0.0','ctx.breakout',(Predicate('features.score','ge',0.6),Predicate('features.direction','eq','long')),Action.ENTER_LONG,'market','standard',(Predicate('features.blocked','eq',True),),(ExceptionRule('thin_liquidity',(Predicate('features.liquidity','lt',0.3),),risk_tier='low',note='reduce risk'),),'pinned manual doctrine',0,999999)
def golden_occurrence(): return ContextOccurrence('occ:1','ctx.breakout',5000,5000,{'score':.8,'direction':'long','blocked':False,'liquidity':.8},('tabular','sequence'),('market','limit'),('low','standard'),('enter_long','no_action'))
def golden_output(): return ModelOutput('model-alpha','1.2.0','occ:1',5000,6000,{'enter_long':.75,'no_action':.25},.22,.81,{'market':.35,'limit':.65},{'low':.2,'standard':.8},.72,.08,.12,.10,CalibrationState.VALID,('tabular','sequence'),h('c'))
def golden_fallback(): return default_fallback_policy()
def golden_authority(): return default_authority_matrix()
def golden_manual_graph(manual=None,fallback=None,authority=None):
    manual=manual or golden_manual(); fallback=fallback or golden_fallback(); authority=authority or golden_authority()
    nodes=(PolicyNodeSpec('input',NodeKind.INPUT,(),Authority.SYSTEM),PolicyNodeSpec('eligibility',NodeKind.MANUAL_ELIGIBILITY,('input',),Authority.MANUAL_POLICY),PolicyNodeSpec('treatment',NodeKind.MANUAL_TREATMENT,('eligibility',),Authority.MANUAL_POLICY),PolicyNodeSpec('veto',NodeKind.MANUAL_VETO,('treatment',),Authority.MANUAL_POLICY),PolicyNodeSpec('output',NodeKind.OUTPUT,('veto',),Authority.SYSTEM))
    return PolicyGraphSpec('graph.manual','1.0.0',PolicyMode.MANUAL_ONLY,nodes,'output',manual.policy_hash,fallback.policy_hash,authority.matrix_hash,('ctx.breakout',),('market','limit'),('low','standard'),('enter_long','no_action'))
def golden_hybrid_graph(admission=None,manual=None,fallback=None,authority=None):
    admission=admission or golden_admission(); manual=manual or golden_manual(); fallback=fallback or golden_fallback(); authority=authority or golden_authority()
    nodes=(PolicyNodeSpec('input',NodeKind.INPUT,(),Authority.SYSTEM),PolicyNodeSpec('eligibility',NodeKind.MANUAL_ELIGIBILITY,('input',),Authority.MANUAL_POLICY),PolicyNodeSpec('manual',NodeKind.MANUAL_TREATMENT,('eligibility',),Authority.MANUAL_POLICY),PolicyNodeSpec('filter',NodeKind.MODEL_FILTER,('manual',),Authority.MODEL,{'action':'enter_long','minimum_probability':.55,'minimum_utility':0.0}),PolicyNodeSpec('rank',NodeKind.MODEL_RANK,('filter',),Authority.MODEL,{'minimum_rank':.5}),PolicyNodeSpec('treatment',NodeKind.MODEL_TREATMENT,('rank',),Authority.MODEL),PolicyNodeSpec('risk',NodeKind.MODEL_RISK,('treatment',),Authority.MODEL),PolicyNodeSpec('veto',NodeKind.MANUAL_VETO,('risk',),Authority.MANUAL_POLICY),PolicyNodeSpec('risk_gate',NodeKind.RISK_GATE,('veto',),Authority.RISK_ENGINE,{'risk_rejected':False}),PolicyNodeSpec('kill',NodeKind.KILL_SWITCH,('risk_gate',),Authority.KILL_SWITCH,{'engaged':False}),PolicyNodeSpec('fallback',NodeKind.FALLBACK,('kill',),Authority.SYSTEM),PolicyNodeSpec('output',NodeKind.OUTPUT,('fallback',),Authority.SYSTEM))
    return PolicyGraphSpec('graph.hybrid','1.0.0',PolicyMode.HYBRID,nodes,'output',manual.policy_hash,fallback.policy_hash,authority.matrix_hash,('ctx.breakout',),('market','limit'),('low','standard'),('enter_long','no_action'),admission.admission_hash)
