from __future__ import annotations
import time
from collections import Counter
from strategy_factory_treatments_v3.enums import TreatmentKind
from .contracts import *
from .compatibility import CompatibilityRuleSet,default_rules
from .errors import CompilationError
from .utils import stable_id,canonical_value

class TreatmentCompiler:
    VERSION='3.1.0'
    def __init__(self,catalog,rules:CompatibilityRuleSet|None=None): self.catalog=catalog; self.rules=rules or default_rules()
    def compile(self,draft:TreatmentDraft,context)->tuple[CompiledTreatment,CompileReport]:
        started=time.perf_counter_ns(); findings=[]
        self._validate_cardinality(draft)
        findings.extend(self._evaluate_intrinsic(draft,context))
        findings.extend(self.rules.evaluate(draft,context,self.catalog))
        fatal=[f for f in findings if not f.passed and f.severity is RuleSeverity.ERROR]
        if fatal:
            report=CompileReport(draft.draft_id,False,tuple(findings),'',(time.perf_counter_ns()-started)//1000,{'fatal_findings':len(fatal)})
            raise CompilationError('compatibility_rejected','treatment draft failed compatibility',{'report':report.to_dict()})
        built={}; management=[]; invocations=[]
        for sel in self._canonical_selections(draft.selections):
            atom=self.catalog.resolve_exact_key(sel.exact_key)
            inv,plan=atom.invoke(context,sel.parameters,{'selection_id':sel.selection_id,'compiler_version':self.VERSION})
            invocations.append(inv)
            if sel.role is TreatmentKind.MANAGEMENT: management.append((sel,plan))
            else: built[sel.role]=(sel,plan)
        self._validate_plan_geometry(context,built,management)
        action_order=self._build_action_order(built,management)
        identity_material={
            'compiler_version':self.VERSION,
            'behavior_draft':{'side':draft.side.value,'runtime_mode':draft.runtime_mode.value,'selections':[x.to_dict() for x in self._canonical_selections(draft.selections)],'intrabar_policy':draft.intrabar_policy.to_dict(),'market_mode':draft.market_mode.value,'account_mode':draft.account_mode.value,'required_capabilities':list(sorted(set(draft.required_capabilities)))},
            'context_occurrence_id':context.context_occurrence_id,
            'feature_frame_hash':context.feature_frame_hash,'decision_time_ms':context.decision_time_ms,
            'descriptor_definition_ids':[x.descriptor_definition_id for x in invocations],
            'invocation_ids':[x.invocation_id for x in invocations],
            'plans':[x[1].to_dict() for x in built.values()]+[p.to_dict() for _,p in management],
            'action_order':[x.to_dict() for x in action_order],
        }
        treatment_id=stable_id('ucet',identity_material)
        treatment=CompiledTreatment(treatment_id,draft.draft_id,context.context_occurrence_id,context.feature_frame_hash,context.side,context.decision_time_ms,
            built[TreatmentKind.ENTRY][1],built[TreatmentKind.STOP][1],built[TreatmentKind.TARGET][1],built[TreatmentKind.TRAILING][1],tuple(p for _,p in management),built[TreatmentKind.SIZING][1],
            tuple(self._canonical_selections(draft.selections)),tuple(action_order),tuple(sorted(set(draft.required_capabilities))),tuple(findings),draft.intrabar_policy,self.VERSION,draft.pinned,
            {'market_mode':draft.market_mode.value,'account_mode':draft.account_mode.value,'compiler_mode':draft.compiler_mode.value,'rule_set':list(self.rules.definition_ids)})
        report=CompileReport(draft.draft_id,True,tuple(findings),treatment_id,(time.perf_counter_ns()-started)//1000,{'atoms':len(draft.selections),'actions':len(action_order),'management_atoms':len(management)})
        return treatment,report
    @staticmethod
    def _canonical_selections(selections): return sorted(selections,key=lambda s:(s.role.value,s.exact_key,s.selection_id))
    @staticmethod
    def _validate_cardinality(draft):
        c=Counter(s.role for s in draft.selections)
        for role in (TreatmentKind.ENTRY,TreatmentKind.STOP,TreatmentKind.TARGET,TreatmentKind.TRAILING,TreatmentKind.SIZING):
            if c[role]!=1: raise CompilationError('invalid_cardinality',f'exactly one {role.value} atom required',{'count':c[role]})
        if c[TreatmentKind.MANAGEMENT]>8: raise CompilationError('management_limit','at most eight management atoms allowed')
        keys=[s.exact_key for s in draft.selections]
        if len(keys)!=len(set((s.role.value,s.exact_key,s.alias) for s in draft.selections)): raise CompilationError('duplicate_selection','duplicate treatment atom selection')
    def _evaluate_intrinsic(self,draft,context):
        findings=[]; selected_ids={s.exact_key.rsplit('@',1)[0] for s in draft.selections}
        for s in draft.selections:
            atom=self.catalog.resolve_exact_key(s.exact_key); d=atom.descriptor
            ok_side=context.side in d.compatibility.supported_sides
            findings.append(RuleFinding(d.definition_id,ok_side,RuleSeverity.ERROR,'side_compatible' if ok_side else 'unsupported_side','side compatibility',{'side':context.side.value}))
            ok_mode=context.runtime_mode in d.compatibility.supported_modes
            findings.append(RuleFinding(d.definition_id,ok_mode,RuleSeverity.ERROR,'mode_compatible' if ok_mode else 'unsupported_mode','runtime compatibility',{'mode':context.runtime_mode.value}))
            missing=sorted(set(d.compatibility.required_context_fields)-context.available_fields)
            findings.append(RuleFinding(d.definition_id,not missing,RuleSeverity.ERROR,'context_fields_present' if not missing else 'missing_context_fields','required context fields',{'missing':missing}))
            conflicts=sorted(set(d.compatibility.incompatible_atom_ids)&selected_ids)
            findings.append(RuleFinding(d.definition_id,not conflicts,RuleSeverity.ERROR,'no_conflict' if not conflicts else 'atom_conflict','atom incompatibility',{'conflicts':conflicts}))
        return findings
    @staticmethod
    def _validate_plan_geometry(context,built,management):
        entry=built[TreatmentKind.ENTRY][1]; stop=built[TreatmentKind.STOP][1]; target=built[TreatmentKind.TARGET][1]
        total=sum((leg.allocation_fraction for leg in entry.legs),start=0)
        if abs(total-1)>1e-9: raise CompilationError('entry_fraction_sum','entry allocation fractions must sum to one',{'sum':str(total)})
        target_total=sum((leg.quantity_fraction for leg in target.legs),start=0)
        if target.no_fixed_target:
            if target_total>1: raise CompilationError('target_fraction_sum','runner target fractions exceed one')
        elif abs(target_total-1)>1e-9: raise CompilationError('target_fraction_sum','target fractions must sum to one',{'sum':str(target_total)})
        if stop.stop_price is not None:
            anchors=[leg.trigger_price for leg in entry.legs]
            if context.side.value=='long' and any(stop.stop_price>=p for p in anchors): raise CompilationError('invalid_stop_side','long stop must be below every entry leg')
            if context.side.value=='short' and any(stop.stop_price<=p for p in anchors): raise CompilationError('invalid_stop_side','short stop must be above every entry leg')
        partial=sum((r.quantity_fraction for _,p in management for r in p.rules if r.rule_type in ('partial_exit_at_r','scale_out')),start=0)
        if partial>1: raise CompilationError('management_exit_fraction','management exit fractions exceed one',{'sum':str(partial)})
        if target.no_fixed_target and built[TreatmentKind.TRAILING][1].mode=='none':
            terminal_rules={'force_exit_after_ms','force_exit_at_time','force_flatten_on_tag'}
            if not any(r.rule_type in terminal_rules for _,p in management for r in p.rules):
                raise CompilationError('runner_without_termination','runner requires trailing or an explicit terminal management rule')
    @staticmethod
    def _build_action_order(built,management):
        rows=[]; seq=0
        def add(phase,typ,sel,plan,priority,payload):
            nonlocal seq; seq+=1; rows.append(ActionStep(seq,phase,typ,sel.exact_key,plan.plan_id,priority,payload))
        sel,plan=built[TreatmentKind.ENTRY]
        for i,leg in enumerate(plan.legs): add('entry','submit_entry_leg',sel,plan,100+i,{'leg_index':i,**leg.to_dict()})
        sel,plan=built[TreatmentKind.STOP]; add('protection','install_initial_stop',sel,plan,10,plan.to_dict())
        sel,plan=built[TreatmentKind.TARGET]
        for i,leg in enumerate(plan.legs): add('exit','install_target_leg',sel,plan,300+i,{'leg_index':i,**leg.to_dict()})
        sel,plan=built[TreatmentKind.TRAILING]; add('management','configure_trailing',sel,plan,500,plan.to_dict())
        for msel,mplan in sorted(management,key=lambda x:(x[0].exact_key,x[1].plan_id)):
            for i,rule in enumerate(mplan.rules): add('management','register_management_rule',msel,mplan,600+i,{'rule_index':i,**rule.to_dict()})
        sel,plan=built[TreatmentKind.SIZING]; add('risk','reserve_sizing_budget',sel,plan,0,plan.to_dict())
        rows.sort(key=lambda x:(x.priority,x.phase,x.source_exact_key,x.sequence))
        return [ActionStep(i+1,x.phase,x.action_type,x.source_exact_key,x.source_plan_id,x.priority,x.payload) for i,x in enumerate(rows)]
