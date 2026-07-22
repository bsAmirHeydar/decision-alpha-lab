from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from strategy_factory_rthp_context_v1 import build_auxiliary_payload, validate_source_record

from .canonical import sha256_material, stable_id, write_json, write_jsonl
from .config import ActivationConfig
from .cycles import CYCLE_DEFINITION_VERSION, NY, CycleAggregate, build_cycles, confirmation_closes, from_ms
from .families import RelationCandidate, build_relation_candidates
from .ticks import Tick, TickSeries, load_tick_jsonl


@dataclass(frozen=True, slots=True)
class MaterializationResult:
    occurrence_ledger: Path
    reference_state_ledger: Path
    cycle_instance_ledger: Path
    role_price_path_ledger: Path
    data_binding: Path
    materialization_report: Path
    occurrence_count: int
    family_counts: dict[str, int]
    source_digest: str


@dataclass(frozen=True, slots=True)
class TouchPair:
    primary: Tick | None
    secondary: Tick | None


class RTHPHistoricalMaterializer:
    def __init__(self, config: ActivationConfig):
        self.config = config
        source = config.data_source
        self.primary = load_tick_jsonl(source.primary_tick_jsonl, source.primary_symbol, source.start_time_ms, source.end_time_ms)
        self.secondary = load_tick_jsonl(source.secondary_tick_jsonl, source.secondary_symbol, source.start_time_ms, source.end_time_ms)
        self.series = {self.primary.symbol: self.primary, self.secondary.symbol: self.secondary}
        self.pair_id = f"{self.primary.symbol}__{self.secondary.symbol}"
        self.source_digest = "sha256:" + sha256_material({
            "primary_hash": self.primary.source_hash,
            "secondary_hash": self.secondary.source_hash,
            "config_digest": config.config_digest,
        })
        self.cycles = build_cycles(self.primary, self.secondary)
        self.candidates = build_relation_candidates(self.cycles)
        self._touch_cache: dict[tuple[str, str], TouchPair] = {}

    def _touch_pair(self, reference: CycleAggregate, side: str) -> TouchPair:
        key = (reference.key.cycle_instance_id, side)
        if key in self._touch_cache:
            return self._touch_cache[key]
        primary_extrema = reference.symbols[self.primary.symbol]
        secondary_extrema = reference.symbols[self.secondary.symbol]
        primary_level = primary_extrema.high if side == "HIGH" else primary_extrema.low
        secondary_level = secondary_extrema.high if side == "HIGH" else secondary_extrema.low
        pair = TouchPair(
            self.primary.first_touch(reference.key.end_ms, side, primary_level),
            self.secondary.first_touch(reference.key.end_ms, side, secondary_level),
        )
        self._touch_cache[key] = pair
        return pair

    @staticmethod
    def _effective_time(tick: Tick | None) -> int | None:
        return None if tick is None else max(tick.event_time_ms, tick.known_time_ms)

    def _fresh_tick(self, series: TickSeries, close_ms: int) -> Tick | None:
        tick = series.latest_at_or_before(close_ms, known_by_ms=close_ms)
        if tick is None or close_ms - tick.event_time_ms > self.config.data_source.max_confirmation_freshness_ms:
            return None
        return tick

    def _active_range_ticks(self, candidate: RelationCandidate, hunter_symbol: str, close_ms: int) -> float | None:
        series = self.series[hunter_symbol]
        ticks = series.between(candidate.active.key.start_ms, close_ms, include_end=True)
        if not ticks:
            return None
        return (max(x.price for x in ticks) - min(x.price for x in ticks)) / series.tick_size

    def _source_record(
        self,
        candidate: RelationCandidate,
        side: str,
        hunter_touch: Tick,
        hunter_symbol: str,
        protected_symbol: str,
        close_ms: int,
        primary_fresh: Tick,
        secondary_fresh: Tick,
    ) -> dict[str, Any]:
        reference = candidate.reference
        primary_ref = reference.symbols[self.primary.symbol]
        secondary_ref = reference.symbols[self.secondary.symbol]
        hunter_ref = reference.symbols[hunter_symbol]
        hunter_level = hunter_ref.high if side == "HIGH" else hunter_ref.low
        protected_ref = reference.symbols[protected_symbol]
        protected_level = protected_ref.high if side == "HIGH" else protected_ref.low
        protected_tick = primary_fresh if protected_symbol == self.primary.symbol else secondary_fresh
        tick_size = self.series[hunter_symbol].tick_size
        protected_tick_size = self.series[protected_symbol].tick_size
        if side == "HIGH":
            overrun = max(0.0, (hunter_touch.price - hunter_level) / tick_size)
            protected_distance = max(0.0, (protected_level - protected_tick.price) / protected_tick_size)
            polarity = "BEARISH_DIVERGENCE"
        else:
            overrun = max(0.0, (hunter_level - hunter_touch.price) / tick_size)
            protected_distance = max(0.0, (protected_tick.price - protected_level) / protected_tick_size)
            polarity = "BULLISH_DIVERGENCE"
        event_material = {
            "context_id": "CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1",
            "context_version": "1.0.2",
            "pair_id": self.pair_id,
            "family": candidate.family,
            "active_cycle_id": candidate.active.key.cycle_instance_id,
            "reference_cycle_id": reference.key.cycle_instance_id,
            "level_side": side,
            "hunter_symbol": hunter_symbol,
            "protected_symbol": protected_symbol,
            "first_touch_time": hunter_touch.event_time_ms,
            "confirmation_close_time": close_ms,
        }
        event_id = stable_id("RTHPEVT_", event_material, 32, True)
        local_close = from_ms(close_ms).astimezone(NY)
        available = candidate.available_reference_count
        required = candidate.required_reference_count
        sufficiency = "FULL" if required == 0 or available >= required else "PARTIAL"
        source_hash = "sha256:" + sha256_material({"source": self.source_digest, "event": event_material})
        record: dict[str, Any] = {
            "context_id": "CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1",
            "context_version": "1.0.2",
            "event_id": event_id,
            "confirmed_context_event": True,
            "family": candidate.family,
            "pair_id": self.pair_id,
            "cycle_definition_version": CYCLE_DEFINITION_VERSION,
            "active_cycle_id": candidate.active.key.cycle_instance_id,
            "reference_cycle_id": reference.key.cycle_instance_id,
            "active_cycle_type": candidate.active_cycle_type,
            "reference_cycle_type": candidate.reference_cycle_type,
            "level_side": side,
            "polarity": polarity,
            "primary_symbol": self.primary.symbol,
            "secondary_symbol": self.secondary.symbol,
            "hunter_symbol": hunter_symbol,
            "protected_symbol": protected_symbol,
            "event_time_ms": hunter_touch.event_time_ms,
            "known_time_ms": close_ms,
            "confirmation_time_ms": close_ms,
            "observation_cut_ms": close_ms,
            "decision_time_ms": close_ms,
            "confirmation_close_time_ms": close_ms,
            "data_status": "VALID" if sufficiency == "FULL" else "PARTIAL_HISTORY",
            "history_sufficiency": sufficiency,
            "available_reference_count": available,
            "required_reference_count": required,
            "reference_age_cycles": candidate.reference_age_cycles,
            "reference_to_active_gap_cycles": candidate.reference_to_active_gap_cycles,
            "sequentiality": candidate.sequentiality,
            "cycle_completeness": candidate.active.key.completeness,
            "is_same_day_reference": candidate.is_same_day_reference,
            "minute_of_session": max(0, int((close_ms - candidate.active.key.start_ms) // 60_000)),
            "minute_of_day_ny": local_close.hour * 60 + local_close.minute,
            "day_of_week_ny": local_close.isoweekday(),
            "active_cycle_progress": min(1.0, max(0.0, (close_ms - candidate.active.key.start_ms) / max(1, candidate.active.key.end_ms - candidate.active.key.start_ms))),
            "simultaneous_family_count": 1,
            "primary_freshness_age_ms": close_ms - primary_fresh.event_time_ms,
            "secondary_freshness_age_ms": close_ms - secondary_fresh.event_time_ms,
            "reference_state_at_cut": "DIVERGENCE_CONFIRMED",
            "trading_day_ny": candidate.active.key.trading_day_ny,
            "source_revision": self.config.data_source.source_revision,
            "source_content_hash": source_hash,
            "hunter_touch_overrun_ticks": overrun,
            "protected_distance_to_level_ticks": protected_distance,
            "reference_range_ticks": (hunter_ref.high - hunter_ref.low) / tick_size,
            "active_range_ticks": self._active_range_ticks(candidate, hunter_symbol, close_ms),
            "auxiliary": {},
        }
        record["auxiliary"] = build_auxiliary_payload(record)
        findings = validate_source_record(record)
        if findings:
            raise ValueError("materialized occurrence is invalid: " + ";".join(findings))
        return record

    def _materialize_occurrences(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        occurrences: list[dict[str, Any]] = []
        state_scopes: dict[tuple[str, str, str], dict[str, Any]] = {}
        emitted: set[tuple[str, str, str, str]] = set()
        allowed_families = set(self.config.family_filter) if self.config.family_filter else None
        for candidate in self.candidates:
            if allowed_families is not None and candidate.family not in allowed_families:
                continue
            if candidate.reference.known_time_ms > candidate.active.key.end_ms:
                continue
            for side in ("HIGH", "LOW"):
                touches = self._touch_pair(candidate.reference, side)
                primary_effective = self._effective_time(touches.primary)
                secondary_effective = self._effective_time(touches.secondary)
                scope_key = (candidate.family, candidate.reference.key.cycle_instance_id, side)
                scope = state_scopes.setdefault(scope_key, {
                    "schema_version": "1.1.0",
                    "pair_id": self.pair_id,
                    "reference_cycle_id": candidate.reference.key.cycle_instance_id,
                    "family": candidate.family,
                    "level_side": side,
                    "state": "UNTOUCHED_BOTH",
                    "primary_first_touch_time_ms": None if touches.primary is None else touches.primary.event_time_ms,
                    "primary_first_touch_known_time_ms": None if touches.primary is None else touches.primary.known_time_ms,
                    "secondary_first_touch_time_ms": None if touches.secondary is None else touches.secondary.event_time_ms,
                    "secondary_first_touch_known_time_ms": None if touches.secondary is None else touches.secondary.known_time_ms,
                    "hunter_symbol": None,
                    "protected_symbol": None,
                    "first_confirmation_close_time_ms": None,
                    "exhaustion_time": None,
                    "exhaustion_known_time_ms": None,
                    "source_revision": self.config.data_source.source_revision,
                    "source_content_hash": self.source_digest,
                })
                for close_ms in confirmation_closes(candidate.active):
                    if close_ms <= candidate.active.key.start_ms or close_ms > candidate.active.key.end_ms:
                        continue
                    primary_fresh = self._fresh_tick(self.primary, close_ms)
                    secondary_fresh = self._fresh_tick(self.secondary, close_ms)
                    if primary_fresh is None or secondary_fresh is None:
                        continue
                    primary_touched = primary_effective is not None and primary_effective <= close_ms
                    secondary_touched = secondary_effective is not None and secondary_effective <= close_ms
                    if primary_touched and secondary_touched:
                        if scope["first_confirmation_close_time_ms"] is None:
                            scope["state"] = "BOTH_SIDES_TOUCHED"
                        else:
                            scope["state"] = "REFERENCE_EXHAUSTED"
                            second_tick = touches.secondary if scope["protected_symbol"] == self.secondary.symbol else touches.primary
                            if second_tick is not None:
                                scope["exhaustion_time"] = datetime.fromtimestamp(second_tick.event_time_ms / 1000, timezone.utc).isoformat().replace("+00:00", "Z")
                                scope["exhaustion_known_time_ms"] = second_tick.known_time_ms
                        break
                    if primary_touched == secondary_touched:
                        continue
                    hunter_tick = touches.primary if primary_touched else touches.secondary
                    if hunter_tick is None:
                        continue
                    hunter_symbol = self.primary.symbol if primary_touched else self.secondary.symbol
                    protected_symbol = self.secondary.symbol if primary_touched else self.primary.symbol
                    emit_key = (candidate.family, candidate.active.key.cycle_instance_id, candidate.reference.key.cycle_instance_id, side)
                    if emit_key in emitted:
                        continue
                    record = self._source_record(candidate, side, hunter_tick, hunter_symbol, protected_symbol, close_ms, primary_fresh, secondary_fresh)
                    occurrences.append(record)
                    emitted.add(emit_key)
                    scope["state"] = "DIVERGENCE_CONFIRMED"
                    scope["hunter_symbol"] = hunter_symbol
                    scope["protected_symbol"] = protected_symbol
                    if scope["first_confirmation_close_time_ms"] is None:
                        scope["first_confirmation_close_time_ms"] = close_ms
                    break
        grouped: dict[tuple[int, str, str, str], int] = {}
        for record in occurrences:
            key = (record["confirmation_close_time_ms"], record["hunter_symbol"], record["protected_symbol"], record["level_side"])
            grouped[key] = grouped.get(key, 0) + 1
        for record in occurrences:
            key = (record["confirmation_close_time_ms"], record["hunter_symbol"], record["protected_symbol"], record["level_side"])
            record["simultaneous_family_count"] = grouped[key]
            record["auxiliary"] = build_auxiliary_payload(record)
            findings = validate_source_record(record)
            if findings:
                raise ValueError("simultaneous-count projection invalid: " + ";".join(findings))
        return sorted(occurrences, key=lambda x: (x["confirmation_close_time_ms"], x["event_id"])), sorted(state_scopes.values(), key=lambda x: (x["family"], x["reference_cycle_id"], x["level_side"]))

    def _cycle_rows(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for cycle in self.cycles:
            symbol_extrema = {}
            for symbol, extrema in sorted(cycle.symbols.items()):
                symbol_extrema[symbol] = {
                    "high": extrema.high,
                    "low": extrema.low,
                    "first_price": extrema.first_price,
                    "last_price": extrema.last_price,
                    "first_time_ms": extrema.first_time_ms,
                    "last_time_ms": extrema.last_time_ms,
                    "tick_count": extrema.tick_count,
                    "tick_size": self.series[symbol].tick_size,
                }
            rows.append({
                "schema_version": "1.1.0",
                "cycle_instance_id": cycle.key.cycle_instance_id,
                "cycle_definition_version": CYCLE_DEFINITION_VERSION,
                "cycle_type": cycle.key.cycle_type,
                "start_time_ms": cycle.key.start_ms,
                "end_time_ms": cycle.key.end_ms,
                "known_time_ms": cycle.known_time_ms,
                "timezone": "America/New_York",
                "trading_day_ny": cycle.key.trading_day_ny,
                "completeness": cycle.key.completeness,
                "symbol_extrema": symbol_extrema,
                "source_revision": self.config.data_source.source_revision,
                "source_content_hash": self.source_digest,
            })
        return rows

    def _role_path_rows(self, occurrences: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        active_by_id = {x.key.cycle_instance_id: x for x in self.cycles}
        for occurrence in occurrences:
            cut = int(occurrence["observation_cut_ms"])
            active = active_by_id[occurrence["active_cycle_id"]]
            end = max(cut + 3_600_000, active.key.end_ms)
            for role, symbol in (("HUNTER", occurrence["hunter_symbol"]), ("PROTECTED", occurrence["protected_symbol"])):
                series = self.series[symbol]
                seed_tick = series.latest_at_or_before(cut, known_by_ms=cut)
                path_ticks = list(series.between(cut, end, include_end=True))
                if seed_tick is not None and (not path_ticks or path_ticks[0].event_time_ms > cut):
                    path_ticks.insert(0, seed_tick)
                for tick in path_ticks:
                    rows.append({
                        "schema_version": "1.1.0",
                        "event_id": occurrence["event_id"],
                        "pair_id": self.pair_id,
                        "evaluation_symbol_role": role,
                        "symbol": symbol,
                        "observation_cut_ms": cut,
                        "active_cycle_end_ms": active.key.end_ms,
                        "observed_at_ms": tick.event_time_ms,
                        "known_time_ms": tick.known_time_ms,
                        "price": tick.price,
                        "price_basis": "BID",
                        "tick_size": tick.tick_size,
                        "source_revision": self.config.data_source.source_revision,
                        "source_content_hash": self.source_digest,
                    })
        return sorted(rows, key=lambda x: (x["event_id"], x["evaluation_symbol_role"], x["observed_at_ms"], x["known_time_ms"]))

    def materialize(self, output_root: Path) -> MaterializationResult:
        ledger_root = output_root / "ledgers"
        occurrence_path = ledger_root / "rthp_canonical_occurrence_ledger.jsonl"
        reference_path = ledger_root / "rthp_reference_state_ledger.jsonl"
        cycle_path = ledger_root / "rthp_cycle_instance_ledger.jsonl"
        role_path = ledger_root / "rthp_role_price_path_ledger.jsonl"
        occurrences, states = self._materialize_occurrences()
        cycles = self._cycle_rows()
        paths = self._role_path_rows(occurrences)
        write_jsonl(occurrence_path, occurrences)
        write_jsonl(reference_path, states)
        write_jsonl(cycle_path, cycles)
        write_jsonl(role_path, paths)
        metadata = {
            "provider": self.config.data_source.provider,
            "symbol_pair": [self.primary.symbol, self.secondary.symbol],
            "date_range": {
                "start_time_ms": min(self.primary.ticks[0].event_time_ms, self.secondary.ticks[0].event_time_ms),
                "end_time_ms": max(self.primary.ticks[-1].event_time_ms, self.secondary.ticks[-1].event_time_ms),
            },
            "timezone": "America/New_York",
            "price_basis": "BID",
            "tick_size_source": self.config.data_source.tick_size_source,
            "contract_roll_policy": self.config.data_source.contract_roll_policy,
            "entitlement_id": self.config.data_source.entitlement_id,
            "producer_version": self.config.data_source.producer_version,
            "availability_time_policy": self.config.data_source.availability_time_policy,
        }
        sources = []
        for source_id, path, schema_ref, known_time_field, label_only in (
            ("RTHP_CANONICAL_OCCURRENCE_LEDGER", occurrence_path, "registry/strategy_factory/contexts/rthp/v1/rthp_ai_source_record.schema.json", "known_time_ms", False),
            ("RTHP_REFERENCE_STATE_LEDGER", reference_path, "registry/strategy_factory/contexts/rthp/v1/rthp_reference_state.schema.json", "exhaustion_known_time_ms", False),
            ("RTHP_CYCLE_INSTANCE_LEDGER", cycle_path, "registry/strategy_factory/contexts/rthp/v1/rthp_ai_cycle_instance.schema.json", "known_time_ms", False),
            ("RTHP_ROLE_PRICE_PATH_LEDGER", role_path, "registry/strategy_factory/contexts/rthp/v1/rthp_ai_role_price_path.schema.json", "known_time_ms", True),
        ):
            sources.append({
                "source_id": source_id,
                "artifact_uri": path.resolve().as_uri(),
                "content_hash": "sha256:" + __import__("hashlib").sha256(path.read_bytes()).hexdigest(),
                "known_time_field": known_time_field,
                "schema_ref": schema_ref,
                "required": True,
                "label_only": label_only,
            })
        binding_material = {
            "schema_version": "1.0.0",
            "binding_id": f"RTHP_AI_DATA_BINDING_{self.config.run_id}",
            "binding_status": "RESOLVED",
            "classification": "RESTRICTED",
            "network_fetch_allowed": False,
            "package_id": "rthp.cross_symbol_cycle_divergence",
            "package_version": "1.0.0",
            "metadata": metadata,
            "sources": sources,
        }
        binding_material["binding_digest"] = sha256_material(binding_material)
        binding_path = output_root / "data_binding.real.v1.json"
        write_json(binding_path, binding_material)
        family_counts: dict[str, int] = {}
        for occurrence in occurrences:
            family_counts[occurrence["family"]] = family_counts.get(occurrence["family"], 0) + 1
        report = {
            "report_id": "RTHP_HISTORICAL_MATERIALIZATION_V1",
            "schema_version": "1.0.0",
            "status": "PASS" if occurrences else "BLOCKED",
            "blocker": None if occurrences else "NO_CONFIRMED_RTHP_OCCURRENCES",
            "run_id": self.config.run_id,
            "source_digest": self.source_digest,
            "cycle_count": len(cycles),
            "relation_candidate_count": len(self.candidates),
            "occurrence_count": len(occurrences),
            "reference_state_count": len(states),
            "role_price_path_count": len(paths),
            "family_counts": family_counts,
            "engine_modified": False,
            "canonical_context_modified": False,
            "entry_treatment_execution_created": False,
        }
        report["report_digest"] = sha256_material(report)
        report_path = output_root / "reports" / "materialization_report.json"
        write_json(report_path, report)
        return MaterializationResult(occurrence_path, reference_path, cycle_path, role_path, binding_path, report_path, len(occurrences), family_counts, self.source_digest)
