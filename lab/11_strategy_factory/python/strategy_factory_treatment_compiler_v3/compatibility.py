from __future__ import annotations
from decimal import Decimal
from strategy_factory_treatments_v3.enums import TreatmentKind
from .contracts import CompatibilityRule,RuleFinding,TreatmentDraft
from .enums import RuleType,RuleSeverity

class CompatibilityRuleSet:
    def __init__(self,rules=()): self._rules=tuple(sorted(rules,key=lambda x:x.exact_key))
    @property
    def rules(self): return self._rules
    @property
    def definition_ids(self): return tuple(r.definition_id for r in self._rules)
    def evaluate(self,draft:TreatmentDraft,context,catalog)->tuple[RuleFinding,...]:
        keys=[s.exact_key for s in draft.selections]; ids=[k.rsplit('@',1)[0] for k in keys]
        tags=set(); kinds=[]
        for s in draft.selections:
            atom=catalog.resolve_exact_key(s.exact_key); kinds.append(atom.descriptor.kind.value); tags.update(atom.descriptor.compatibility.tags)
        findings=[]
        for r in self._rules:
            if r.applies_to_modes and draft.runtime_mode.value not in r.applies_to_modes: continue
            passed=True; evidence={}
            if r.rule_type is RuleType.REQUIRE_ATOM: passed=r.object_value in ids or r.object_value in keys
            elif r.rule_type is RuleType.PROHIBIT_ATOM: passed=not (r.object_value in ids or r.object_value in keys)
            elif r.rule_type is RuleType.REQUIRE_TAG: passed=r.object_value in tags
            elif r.rule_type is RuleType.PROHIBIT_TAG: passed=r.object_value not in tags
            elif r.rule_type is RuleType.REQUIRE_CONTEXT_FIELD: passed=r.object_value in context.available_fields
            elif r.rule_type is RuleType.REQUIRE_CAPABILITY: passed=r.object_value in draft.required_capabilities
            elif r.rule_type is RuleType.MARKET_MODE: passed=draft.market_mode.value in (r.object_value,'any')
            elif r.rule_type is RuleType.ACCOUNT_MODE: passed=draft.account_mode.value in (r.object_value,'any')
            elif r.rule_type is RuleType.MAX_COUNT:
                count=sum(1 for s in draft.selections if s.role.value==r.subject); passed=count<=int(r.threshold or 0); evidence={'count':count}
            elif r.rule_type is RuleType.PARAMETER_RELATION:
                left=self._find_param(draft,r.subject); right=self._parse_operand(draft,r.object_value); passed=self._compare(left,right,r.operator); evidence={'left':str(left),'right':str(right),'operator':r.operator}
            elif r.rule_type is RuleType.QUANTITY_SUM:
                total=sum(Decimal(str(s.parameters.get(r.subject,0))) for s in draft.selections if r.subject in s.parameters); passed=self._compare(total,Decimal(str(r.threshold or 1)),r.operator or '<='); evidence={'total':str(total)}
            findings.append(RuleFinding(r.definition_id,passed,r.severity,'ok' if passed else f'rule_failed:{r.rule_id}',r.message or r.rule_id,evidence))
        return tuple(findings)
    @staticmethod
    def _find_param(draft,path):
        # path syntax exact_key:param or atom_id:param
        atom,param=path.split(':',1)
        for s in draft.selections:
            if s.exact_key==atom or s.exact_key.rsplit('@',1)[0]==atom:
                if param not in s.parameters: raise ValueError(f'parameter not supplied for rule: {path}')
                return Decimal(str(s.parameters[param]))
        raise ValueError(f'atom not found for rule: {atom}')
    def _parse_operand(self,draft,value):
        if ':' in value:
            try:return self._find_param(draft,value)
            except ValueError: pass
        return Decimal(str(value))
    @staticmethod
    def _compare(a,b,op):
        return {'<':a<b,'<=':a<=b,'==':a==b,'!=':a!=b,'>=':a>=b,'>':a>b}.get(op,False)

def default_rules()->CompatibilityRuleSet:
    R=CompatibilityRule; T=RuleType; S=RuleSeverity
    return CompatibilityRuleSet((
        R('core.one_entry','1.0.0',T.MAX_COUNT,S.ERROR,'entry','',threshold=Decimal('1'),message='exactly one entry atom is allowed'),
        R('core.one_stop','1.0.0',T.MAX_COUNT,S.ERROR,'stop','',threshold=Decimal('1'),message='exactly one stop atom is allowed'),
        R('core.one_target','1.0.0',T.MAX_COUNT,S.ERROR,'target','',threshold=Decimal('1'),message='exactly one target atom is allowed'),
        R('core.one_trailing','1.0.0',T.MAX_COUNT,S.ERROR,'trailing','',threshold=Decimal('1'),message='exactly one trailing atom is allowed'),
        R('core.one_sizing','1.0.0',T.MAX_COUNT,S.ERROR,'sizing','',threshold=Decimal('1'),message='exactly one sizing atom is allowed'),
        R('live.requires_broker_guard','1.0.0',T.REQUIRE_CAPABILITY,S.ERROR,'','broker_preflight',message='live treatments require broker_preflight capability',applies_to_modes=('live',)),
    ))
