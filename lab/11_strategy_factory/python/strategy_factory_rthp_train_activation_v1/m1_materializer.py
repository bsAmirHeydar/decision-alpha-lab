from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from strategy_factory_rthp_context_v1 import build_auxiliary_payload, validate_source_record

from .canonical import sha256_file, sha256_material, stable_id, write_json, write_jsonl
from .config import ActivationConfig
from .cycles import CYCLE_DEFINITION_VERSION, CycleKey, NY, confirmation_closes, cycle_keys_for_tick, from_ms
from .families import RelationCandidate, build_relation_candidates
from .m1_bars import M1Bar, M1BarSeries, M1Touch, load_m1_bar_jsonl
from .materializer import MaterializationResult


@dataclass(slots=True)
class BarExtrema:
    high: float = float("-inf")
    low: float = float("inf")
    first_price: float | None = None
    last_price: float | None = None
    first_time_ms: int | None = None
    last_time_ms: int | None = None
    max_known_time_ms: int = 0
    bar_count: int = 0

    def update(self, bar: M1Bar) -> None:
        self.high = max(self.high, bar.high)
        self.low = min(self.low, bar.low)
        if self.first_price is None:
            self.first_price = bar.open
            self.first_time_ms = bar.open_time_ms
        self.last_price = bar.close
        self.last_time_ms = bar.close_time_ms
        self.max_known_time_ms = max(self.max_known_time_ms, bar.known_time_ms)
        self.bar_count += 1


@dataclass(slots=True)
class BarCycleAggregate:
    key: CycleKey
    symbols: dict[str, BarExtrema] = field(default_factory=dict)

    def update(self, bar: M1Bar) -> None:
        self.symbols.setdefault(bar.symbol, BarExtrema()).update(bar)

    def complete_for(self, primary: str, secondary: str) -> bool:
        return primary in self.symbols and secondary in self.symbols

    @property
    def known_time_ms(self) -> int:
        return max([self.key.end_ms, *(x.max_known_time_ms for x in self.symbols.values())])


@dataclass(frozen=True, slots=True)
class BarTouchPair:
    primary: M1Touch | None
    secondary: M1Touch | None


def _keys_for_bar(bar: M1Bar) -> tuple[CycleKey, ...]:
    class Proxy:
        event_time_ms = bar.open_time_ms
    return cycle_keys_for_tick(Proxy())


def build_bar_cycles(primary: M1BarSeries, secondary: M1BarSeries) -> tuple[BarCycleAggregate, ...]:
    cycles: dict[tuple[str, int, int], BarCycleAggregate] = {}
    all_bars = sorted((*primary.bars, *secondary.bars), key=lambda x: (x.open_time_ms, x.symbol, x.source_sequence))
    for bar in all_bars:
        for key in _keys_for_bar(bar):
            if not (key.start_ms <= bar.open_time_ms and bar.close_time_ms <= key.end_ms):
                continue
            cycles.setdefault((key.cycle_type, key.start_ms, key.end_ms), BarCycleAggregate(key)).update(bar)
    min_open = min(primary.bars[0].open_time_ms, secondary.bars[0].open_time_ms)
    max_close = max(primary.bars[-1].close_time_ms, secondary.bars[-1].close_time_ms)
    out: list[BarCycleAggregate] = []
    for aggregate in cycles.values():
        if not aggregate.complete_for(primary.symbol, secondary.symbol):
            continue
        if aggregate.key.start_ms < min_open or aggregate.key.end_ms > max_close:
            if aggregate.key.completeness == "COMPLETE":
                aggregate.key = CycleKey(aggregate.key.cycle_type, aggregate.key.start_ms, aggregate.key.end_ms,
                                         aggregate.key.trading_day_ny, "PARTIAL")
        out.append(aggregate)
    return tuple(sorted(out, key=lambda x: (x.key.start_ms, x.key.cycle_type, x.key.end_ms)))


class RTHPM1HistoricalMaterializer:
    """M1-only, interval-censored RTHP materializer; never synthesizes ticks."""

    def __init__(self, config: ActivationConfig):
        self.config = config
        source = config.data_source
        if source.primary_m1_bar_jsonl is None or source.secondary_m1_bar_jsonl is None:
            raise ValueError("M1 materializer requires paired M1 bar sources")
        self.primary = load_m1_bar_jsonl(source.primary_m1_bar_jsonl, source.primary_symbol, source.start_time_ms, source.end_time_ms)
        self.secondary = load_m1_bar_jsonl(source.secondary_m1_bar_jsonl, source.secondary_symbol, source.start_time_ms, source.end_time_ms)
        self.series = {self.primary.symbol: self.primary, self.secondary.symbol: self.secondary}
        self.pair_id = f"{self.primary.symbol}__{self.secondary.symbol}"
        self.source_digest = "sha256:" + sha256_material({"primary_hash": self.primary.source_hash, "secondary_hash": self.secondary.source_hash,
                                                           "mode": "PAIRED_M1_BAR_JSONL", "config_digest": config.config_digest})
        self.cycles = build_bar_cycles(self.primary, self.secondary)
        self.candidates = build_relation_candidates(self.cycles)  # structural duck typing is intentional
        self._touch_cache: dict[tuple[str, str], BarTouchPair] = {}

    def _touch_pair(self, reference: BarCycleAggregate, side: str) -> BarTouchPair:
        key = (reference.key.cycle_instance_id, side)
        if key in self._touch_cache:
            return self._touch_cache[key]
        p, s = reference.symbols[self.primary.symbol], reference.symbols[self.secondary.symbol]
        pair = BarTouchPair(self.primary.first_touch(reference.key.end_ms, side, p.high if side == "HIGH" else p.low),
                            self.secondary.first_touch(reference.key.end_ms, side, s.high if side == "HIGH" else s.low))
        self._touch_cache[key] = pair
        return pair

    def _fresh_bar(self, series: M1BarSeries, close_ms: int) -> M1Bar | None:
        bar = series.latest_closed_at_or_before(close_ms, known_by_ms=close_ms)
        if bar is None or bar.close_time_ms != close_ms:
            return None
        return bar

    def _confirmation_coverage(self, close_ms: int) -> bool:
        start = close_ms - 15 * 60_000
        return self.primary.has_exact_interval(start, close_ms) and self.secondary.has_exact_interval(start, close_ms)

    def _active_range_ticks(self, candidate: RelationCandidate, symbol: str, close_ms: int) -> float | None:
        bars = self.series[symbol].between(candidate.active.key.start_ms, close_ms, include_end=True)
        return None if not bars else (max(x.high for x in bars) - min(x.low for x in bars)) / self.series[symbol].tick_size

    def _source_record(self, candidate: RelationCandidate, side: str, touch: M1Touch, hunter: str, protected: str,
                       close_ms: int, pbar: M1Bar, sbar: M1Bar) -> dict[str, Any]:
        ref = candidate.reference
        h_ref = ref.symbols[hunter]
        pr_ref = ref.symbols[protected]
        h_level = h_ref.high if side == "HIGH" else h_ref.low
        pr_level = pr_ref.high if side == "HIGH" else pr_ref.low
        protected_bar = pbar if protected == self.primary.symbol else sbar
        htick = self.series[hunter].tick_size
        ptick = self.series[protected].tick_size
        if side == "HIGH":
            overrun = max(0.0, (touch.touch_price - h_level) / htick)
            distance = max(0.0, (pr_level - protected_bar.close) / ptick)
            polarity = "BEARISH_DIVERGENCE"
        else:
            overrun = max(0.0, (h_level - touch.touch_price) / htick)
            distance = max(0.0, (protected_bar.close - pr_level) / ptick)
            polarity = "BULLISH_DIVERGENCE"
        event_material = {"context_id":"CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1","context_version":"1.0.2","pair_id":self.pair_id,
                          "family":candidate.family,"active_cycle_id":candidate.active.key.cycle_instance_id,"reference_cycle_id":ref.key.cycle_instance_id,
                          "level_side":side,"hunter_symbol":hunter,"protected_symbol":protected,
                          "first_observable_touch_time":touch.observable_time_ms,"confirmation_close_time":close_ms,"time_resolution":"M1_INTERVAL"}
        event_id = stable_id("RTHPEVT_", event_material, 32, True)
        local = from_ms(close_ms).astimezone(NY)
        available, required = candidate.available_reference_count, candidate.required_reference_count
        suff = "FULL" if required == 0 or available >= required else "PARTIAL"
        source_hash = "sha256:" + sha256_material({"source":self.source_digest,"event":event_material})
        record: dict[str, Any] = {
            "context_id":"CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1","context_version":"1.0.2","event_id":event_id,
            "confirmed_context_event":True,"family":candidate.family,"pair_id":self.pair_id,"cycle_definition_version":CYCLE_DEFINITION_VERSION,
            "active_cycle_id":candidate.active.key.cycle_instance_id,"reference_cycle_id":ref.key.cycle_instance_id,
            "active_cycle_type":candidate.active_cycle_type,"reference_cycle_type":candidate.reference_cycle_type,"level_side":side,"polarity":polarity,
            "primary_symbol":self.primary.symbol,"secondary_symbol":self.secondary.symbol,"hunter_symbol":hunter,"protected_symbol":protected,
            "event_time_ms":touch.observable_time_ms,"known_time_ms":close_ms,"confirmation_time_ms":close_ms,"observation_cut_ms":close_ms,
            "decision_time_ms":close_ms,"confirmation_close_time_ms":close_ms,"data_status":"VALID" if suff == "FULL" else "PARTIAL_HISTORY",
            "history_sufficiency":suff,"available_reference_count":available,"required_reference_count":required,
            "reference_age_cycles":candidate.reference_age_cycles,"reference_to_active_gap_cycles":candidate.reference_to_active_gap_cycles,
            "sequentiality":candidate.sequentiality,"cycle_completeness":candidate.active.key.completeness,
            "is_same_day_reference":candidate.is_same_day_reference,"minute_of_session":max(0,int((close_ms-candidate.active.key.start_ms)//60_000)),
            "minute_of_day_ny":local.hour*60+local.minute,"day_of_week_ny":local.isoweekday(),
            "active_cycle_progress":min(1.0,max(0.0,(close_ms-candidate.active.key.start_ms)/max(1,candidate.active.key.end_ms-candidate.active.key.start_ms))),
            "simultaneous_family_count":1,"primary_freshness_age_ms":close_ms-pbar.close_time_ms,
            "secondary_freshness_age_ms":close_ms-sbar.close_time_ms,"reference_state_at_cut":"DIVERGENCE_CONFIRMED",
            "trading_day_ny":candidate.active.key.trading_day_ny,"source_revision":self.config.data_source.source_revision,
            "source_content_hash":source_hash,"hunter_touch_overrun_ticks":overrun,"protected_distance_to_level_ticks":distance,
            "reference_range_ticks":(h_ref.high-h_ref.low)/htick,"active_range_ticks":self._active_range_ticks(candidate,hunter,close_ms),"auxiliary":{},
        }
        record["auxiliary"] = build_auxiliary_payload(record)
        findings = validate_source_record(record)
        if findings:
            raise ValueError("M1 materialized occurrence invalid: " + ";".join(findings))
        return record

    def _materialize_occurrences(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        occurrences: list[dict[str, Any]] = []
        states: dict[tuple[str,str,str],dict[str,Any]] = {}
        emitted: set[tuple[str,str,str,str]] = set()
        allowed = set(self.config.family_filter) if self.config.family_filter else None
        for candidate in self.candidates:
            if allowed is not None and candidate.family not in allowed:
                continue
            if candidate.reference.known_time_ms > candidate.active.key.end_ms:
                continue
            for side in ("HIGH","LOW"):
                touches = self._touch_pair(candidate.reference, side)
                peff = None if touches.primary is None else touches.primary.observable_time_ms
                seff = None if touches.secondary is None else touches.secondary.observable_time_ms
                skey=(candidate.family,candidate.reference.key.cycle_instance_id,side)
                state=states.setdefault(skey,{"schema_version":"1.1.0","pair_id":self.pair_id,
                    "reference_cycle_id":candidate.reference.key.cycle_instance_id,"family":candidate.family,"level_side":side,"state":"UNTOUCHED_BOTH",
                    "primary_first_touch_time_ms":None if touches.primary is None else touches.primary.interval_start_ms,
                    "primary_first_touch_known_time_ms":None if touches.primary is None else touches.primary.known_time_ms,
                    "secondary_first_touch_time_ms":None if touches.secondary is None else touches.secondary.interval_start_ms,
                    "secondary_first_touch_known_time_ms":None if touches.secondary is None else touches.secondary.known_time_ms,
                    "hunter_symbol":None,"protected_symbol":None,"first_confirmation_close_time_ms":None,"exhaustion_time":None,"exhaustion_known_time_ms":None,
                    "touch_time_resolution":"M1_INTERVAL","intrabar_order":"UNKNOWN","source_revision":self.config.data_source.source_revision,
                    "source_content_hash":self.source_digest})
                for close_ms in confirmation_closes(candidate.active):
                    if close_ms <= candidate.active.key.start_ms or close_ms > candidate.active.key.end_ms or not self._confirmation_coverage(close_ms):
                        continue
                    pbar,sbar=self._fresh_bar(self.primary,close_ms),self._fresh_bar(self.secondary,close_ms)
                    if pbar is None or sbar is None:
                        continue
                    pt=peff is not None and peff<=close_ms
                    st=seff is not None and seff<=close_ms
                    if pt and st:
                        if state["first_confirmation_close_time_ms"] is None:
                            state["state"]="BOTH_SIDES_TOUCHED"
                        else:
                            state["state"]="REFERENCE_EXHAUSTED"
                            second=touches.secondary if state["protected_symbol"]==self.secondary.symbol else touches.primary
                            if second:
                                state["exhaustion_time"]=datetime.fromtimestamp(second.interval_start_ms/1000,timezone.utc).isoformat().replace("+00:00","Z")
                                state["exhaustion_known_time_ms"]=second.known_time_ms
                        break
                    if pt==st:
                        continue
                    touch=touches.primary if pt else touches.secondary
                    if touch is None:
                        continue
                    hunter=self.primary.symbol if pt else self.secondary.symbol
                    protected=self.secondary.symbol if pt else self.primary.symbol
                    ekey=(candidate.family,candidate.active.key.cycle_instance_id,candidate.reference.key.cycle_instance_id,side)
                    if ekey in emitted:
                        continue
                    occurrences.append(self._source_record(candidate,side,touch,hunter,protected,close_ms,pbar,sbar))
                    emitted.add(ekey)
                    state.update({"state":"DIVERGENCE_CONFIRMED","hunter_symbol":hunter,"protected_symbol":protected})
                    if state["first_confirmation_close_time_ms"] is None:
                        state["first_confirmation_close_time_ms"]=close_ms
                    break
        grouped: dict[tuple[int,str,str,str],int]={}
        for r in occurrences:
            k=(r["confirmation_close_time_ms"],r["hunter_symbol"],r["protected_symbol"],r["level_side"]); grouped[k]=grouped.get(k,0)+1
        for r in occurrences:
            k=(r["confirmation_close_time_ms"],r["hunter_symbol"],r["protected_symbol"],r["level_side"]); r["simultaneous_family_count"]=grouped[k]
            r["auxiliary"]=build_auxiliary_payload(r)
            findings=validate_source_record(r)
            if findings: raise ValueError("M1 simultaneous projection invalid: "+";".join(findings))
        return sorted(occurrences,key=lambda x:(x["confirmation_close_time_ms"],x["event_id"])), sorted(states.values(),key=lambda x:(x["family"],x["reference_cycle_id"],x["level_side"]))

    def _cycle_rows(self) -> list[dict[str,Any]]:
        rows=[]
        for cycle in self.cycles:
            ext={}
            for symbol,e in sorted(cycle.symbols.items()):
                ext[symbol]={"high":e.high,"low":e.low,"first_price":e.first_price,"last_price":e.last_price,"first_time_ms":e.first_time_ms,
                             "last_time_ms":e.last_time_ms,"bar_count":e.bar_count,"tick_size":self.series[symbol].tick_size,"source_resolution":"M1"}
            rows.append({"schema_version":"1.1.0","cycle_instance_id":cycle.key.cycle_instance_id,"cycle_definition_version":CYCLE_DEFINITION_VERSION,
                         "cycle_type":cycle.key.cycle_type,"start_time_ms":cycle.key.start_ms,"end_time_ms":cycle.key.end_ms,"known_time_ms":cycle.known_time_ms,
                         "timezone":"America/New_York","trading_day_ny":cycle.key.trading_day_ny,"completeness":cycle.key.completeness,
                         "symbol_extrema":ext,"source_revision":self.config.data_source.source_revision,"source_content_hash":self.source_digest})
        return rows

    def _role_path_rows(self, occurrences: list[dict[str,Any]]) -> list[dict[str,Any]]:
        rows=[]; active_by_id={x.key.cycle_instance_id:x for x in self.cycles}
        for occurrence in occurrences:
            cut=int(occurrence["observation_cut_ms"]); active=active_by_id[occurrence["active_cycle_id"]]; end=max(cut+3_600_000,active.key.end_ms)
            for role,symbol in (("HUNTER",occurrence["hunter_symbol"]),("PROTECTED",occurrence["protected_symbol"])):
                series=self.series[symbol]
                # Seed every label path with the last bar that was fully known at the
                # observation cut. This supplies the causal start price without
                # synthesizing an intrabar price or looking past the cut.
                seed = series.latest_closed_at_or_before(cut, known_by_ms=cut)
                selected_bars = []
                if seed is not None:
                    selected_bars.append(seed)
                selected_bars.extend(series.between(cut,end,include_end=True))
                seen_intervals: set[tuple[int,int]] = set()
                for bar in selected_bars:
                    interval = (bar.open_time_ms, bar.close_time_ms)
                    if interval in seen_intervals:
                        continue
                    seen_intervals.add(interval)
                    rows.append({"schema_version":"1.1.0","event_id":occurrence["event_id"],"pair_id":self.pair_id,"evaluation_symbol_role":role,
                                 "symbol":symbol,"observation_cut_ms":cut,"active_cycle_end_ms":active.key.end_ms,
                                 "observed_at_ms":bar.close_time_ms,"known_time_ms":bar.known_time_ms,"price":bar.close,"open":bar.open,"high":bar.high,
                                 "low":bar.low,"close":bar.close,"interval_start_ms":bar.open_time_ms,"interval_end_ms":bar.close_time_ms,
                                 "time_resolution":"M1_INTERVAL","intrabar_order":"UNKNOWN","price_basis":"BID","tick_size":bar.tick_size,
                                 "source_revision":self.config.data_source.source_revision,"source_content_hash":self.source_digest})
        return sorted(rows,key=lambda x:(x["event_id"],x["evaluation_symbol_role"],x["observed_at_ms"]))

    def materialize(self, output_root: Path) -> MaterializationResult:
        ledger=output_root/"ledgers"; op=ledger/"rthp_canonical_occurrence_ledger.jsonl"; rp=ledger/"rthp_reference_state_ledger.jsonl"
        cp=ledger/"rthp_cycle_instance_ledger.jsonl"; pp=ledger/"rthp_role_price_path_ledger.jsonl"
        occurrences,states=self._materialize_occurrences(); cycles=self._cycle_rows(); paths=self._role_path_rows(occurrences)
        write_jsonl(op,occurrences); write_jsonl(rp,states); write_jsonl(cp,cycles); write_jsonl(pp,paths)
        ppath,spath=self.config.data_source.source_paths
        metadata={"provider":self.config.data_source.provider,"symbol_pair":[self.primary.symbol,self.secondary.symbol],
                  "date_range":{"start_time_ms":max(self.primary.bars[0].open_time_ms,self.secondary.bars[0].open_time_ms),
                                "end_time_ms":min(self.primary.bars[-1].close_time_ms,self.secondary.bars[-1].close_time_ms)},
                  "timezone":"America/New_York","source_time_basis":"UTC","canonical_source_timeframe":"M1_CLOSED_BARS","sub_m1_source_allowed":False,
                  "price_basis":"BID","tick_size_source":self.config.data_source.tick_size_source,"contract_roll_policy":self.config.data_source.contract_roll_policy,
                  "entitlement_id":self.config.data_source.entitlement_id,"producer_version":self.config.data_source.producer_version,
                  "availability_time_policy":self.config.data_source.availability_time_policy}
        sources=[]
        for sid,path,schema,known,label_only in (("RTHP_CANONICAL_OCCURRENCE_LEDGER",op,"registry/strategy_factory/contexts/rthp/v1/rthp_ai_source_record.schema.json","known_time_ms",False),
            ("RTHP_REFERENCE_STATE_LEDGER",rp,"registry/strategy_factory/contexts/rthp/v1/rthp_reference_state.schema.json","exhaustion_known_time_ms",False),
            ("RTHP_CYCLE_INSTANCE_LEDGER",cp,"registry/strategy_factory/contexts/rthp/v1/rthp_ai_cycle_instance.schema.json","known_time_ms",False),
            ("RTHP_ROLE_PRICE_PATH_LEDGER",pp,"registry/strategy_factory/contexts/rthp/v1/rthp_ai_role_price_path.schema.json","known_time_ms",True)):
            sources.append({"source_id":sid,"artifact_uri":path.resolve().as_uri(),"content_hash":"sha256:"+sha256_file(path),"known_time_field":known,
                            "schema_ref":schema,"required":True,"label_only":label_only})
        binding={"schema_version":"1.0.0","binding_id":f"RTHP_AI_DATA_BINDING_{self.config.run_id}","binding_status":"RESOLVED",
                 "classification":"RESTRICTED","network_fetch_allowed":False,"package_id":"rthp.cross_symbol_cycle_divergence","package_version":"1.0.0",
                 "metadata":metadata,"raw_source_artifacts":[{"symbol":self.primary.symbol,"uri":ppath.resolve().as_uri(),"hash":"sha256:"+self.primary.source_hash},
                                                             {"symbol":self.secondary.symbol,"uri":spath.resolve().as_uri(),"hash":"sha256:"+self.secondary.source_hash}],
                 "sources":sources}; binding["binding_digest"]=sha256_material(binding)
        bp=output_root/"data_binding.real.v1.json"; write_json(bp,binding)
        counts={}
        for o in occurrences: counts[o["family"]]=counts.get(o["family"],0)+1
        report={"report_id":"RTHP_M1_HISTORICAL_MATERIALIZATION_V1","schema_version":"1.0.0","status":"PASS" if occurrences else "BLOCKED",
                "blocker":None if occurrences else "NO_CONFIRMED_RTHP_OCCURRENCES","run_id":self.config.run_id,"source_digest":self.source_digest,
                "source_mode":"PAIRED_M1_BAR_JSONL","canonical_source_timeframe":"M1_CLOSED_BARS","synthetic_ticks_created":False,
                "intrabar_order_inferred":False,"cycle_count":len(cycles),"relation_candidate_count":len(self.candidates),"occurrence_count":len(occurrences),
                "reference_state_count":len(states),"role_price_path_count":len(paths),"family_counts":counts,"engine_modified":False,
                "canonical_context_modified":False,"entry_treatment_execution_created":False}; report["report_digest"]=sha256_material(report)
        report_path=output_root/"reports"/"materialization_report.json"; write_json(report_path,report)
        return MaterializationResult(op,rp,cp,pp,bp,report_path,len(occurrences),counts,self.source_digest)
