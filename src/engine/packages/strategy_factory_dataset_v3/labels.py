from __future__ import annotations
from collections import defaultdict
from decimal import Decimal
from typing import Iterable
from .canonical import sha256
from .contracts import *
from .enums import *

class LabelCompiler:
    def _eligible(self,cell:OutcomeCell,task:LabelTaskContract)->tuple[bool,str]:
        policies=set(task.maturity_policies)
        if LabelMaturityPolicy.REQUIRE_RESOLVED in policies and cell.state!=OutcomeState.RESOLVED:return False,"requires_resolved_outcome"
        if cell.state==OutcomeState.UNFILLED and LabelMaturityPolicy.ALLOW_UNFILLED not in policies:return False,"unfilled_not_allowed"
        if cell.maturity.censoring==CensoringKind.RIGHT and LabelMaturityPolicy.ALLOW_RIGHT_CENSORED not in policies:return False,"right_censoring_not_allowed"
        if task.allowed_terminal_reasons and cell.terminal_reason.value not in task.allowed_terminal_reasons:return False,"terminal_reason_not_allowed"
        return True,""
    def compile(self,cube:OutcomeCube,task:LabelTaskContract,known_time_ms:int)->tuple[LabelRecord,...]:
        cells=[c for c in cube.cells if c.scenario_key==task.scenario_key and c.horizon_ms==task.horizon_ms]
        cells.sort(key=lambda c:c.treatment_id)
        if not cells:return ()
        metrics={c.treatment_id:c.metric(task.metric) for c in cells}
        reverse=task.direction==UtilityDirection.MAXIMIZE
        ranked=sorted(cells,key=lambda c:(metrics[c.treatment_id],c.treatment_id),reverse=reverse)
        rank_map={c.treatment_id:i+1 for i,c in enumerate(ranked)}
        all_eligible=all(self._eligible(c,task)[0] for c in cells)
        best=ranked[0].treatment_id if ranked else ""
        out=[]
        for c in cells:
            ok,reason=self._eligible(c,task)
            if LabelMaturityPolicy.REQUIRE_ALL_SIBLINGS in task.maturity_policies and not all_eligible: ok=False; reason="sibling_set_not_fully_mature"
            value=metrics[c.treatment_id]
            kw=dict(opportunity_id=c.opportunity_id,treatment_id=c.treatment_id,task_key=task.exact_key,cell_id=c.cell_id,mature=ok,mask=not ok,sample_weight=Decimal("1"),known_time_ms=known_time_ms,reason=reason,evidence_hash=sha256({"cell":c.to_dict(),"task":task.to_dict()}))
            if not ok: out.append(LabelRecord(**kw)); continue
            if task.task_kind==TaskKind.BINARY:
                positive=value>=task.threshold if task.direction==UtilityDirection.MAXIMIZE else value<=task.threshold
                out.append(LabelRecord(**kw,class_value=1 if positive else 0,scalar_value=value))
            elif task.task_kind in (TaskKind.REGRESSION,TaskKind.QUANTILE): out.append(LabelRecord(**kw,scalar_value=value))
            elif task.task_kind==TaskKind.RANKING: out.append(LabelRecord(**kw,scalar_value=value,rank=rank_map[c.treatment_id]))
            elif task.task_kind==TaskKind.TREATMENT_CHOICE: out.append(LabelRecord(**kw,category_value=best,class_value=1 if c.treatment_id==best else 0,rank=rank_map[c.treatment_id]))
            elif task.task_kind==TaskKind.SURVIVAL:
                duration=(c.exit_time_ms or c.maturity.observation_end_ms)-(c.entry_time_ms or c.maturity.observation_end_ms)
                out.append(LabelRecord(**kw,duration_ms=max(0,duration),event_observed=c.state==OutcomeState.RESOLVED,competing_event=c.terminal_reason.value))
            elif task.task_kind==TaskKind.COMPETING_RISK:
                duration=(c.exit_time_ms or c.maturity.observation_end_ms)-(c.entry_time_ms or c.maturity.observation_end_ms)
                out.append(LabelRecord(**kw,duration_ms=max(0,duration),event_observed=c.state==OutcomeState.RESOLVED,competing_event=c.terminal_reason.value))
            elif task.task_kind==TaskKind.MULTI_TASK: out.append(LabelRecord(**kw,vector_value=(c.net_r,c.mfe_r,c.mae_r,c.max_drawdown_r),scalar_value=value))
            elif task.task_kind==TaskKind.NOVELTY: out.append(LabelRecord(**kw,class_value=int(c.diagnostics.get("novelty",0)),scalar_value=value))
            elif task.task_kind==TaskKind.BOUNDED_POLICY:
                floor=task.bounded_min_utility if task.bounded_min_utility is not None else task.threshold
                allowed=value>=floor if task.direction==UtilityDirection.MAXIMIZE else value<=floor
                out.append(LabelRecord(**kw,class_value=1 if allowed else 0,scalar_value=value,category_value=c.treatment_id if allowed else ""))
        return tuple(out)
