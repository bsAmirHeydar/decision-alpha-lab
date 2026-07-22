from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class CompiledLabel:
    event_id: str
    task_id: str
    label_contract_id: str
    kind: str
    target: float
    maturity_time_ms: int
    known_time_ms: int
    ranking_group: str
    censor_event: int
    censor_duration_ms: int


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class RTHPLabelCompiler:
    def __init__(self, task_registry_path: Path, label_bindings_path: Path):
        self.tasks = json.loads(task_registry_path.read_text(encoding="utf-8"))["tasks"]
        labels = json.loads(label_bindings_path.read_text(encoding="utf-8"))["labels"]
        self.labels = {x["label_contract_id"]: x for x in labels}

    @staticmethod
    def _path_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
        index: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in rows:
            index.setdefault((row["event_id"], row["evaluation_symbol_role"]), []).append(row)
        for key in index:
            index[key].sort(key=lambda x: (x["observed_at_ms"], x["known_time_ms"]))
        return index

    @staticmethod
    def _state_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str, str], dict[str, Any]]:
        return {(x["family"], x["reference_cycle_id"], x["level_side"]): x for x in rows}

    @staticmethod
    def _price_at(path: list[dict[str, Any]], time_ms: int, *, known_by_ms: int) -> float | None:
        candidates = [x for x in path if x["observed_at_ms"] <= time_ms and x["known_time_ms"] <= known_by_ms]
        return None if not candidates else float(candidates[-1].get("close", candidates[-1]["price"]))

    @staticmethod
    def _window(path: list[dict[str, Any]], start_ms: int, end_ms: int, *, known_by_ms: int) -> list[dict[str, Any]]:
        return [x for x in path if start_ms <= x["observed_at_ms"] <= end_ms and x["known_time_ms"] <= known_by_ms]

    @staticmethod
    def _sign(occurrence: dict[str, Any]) -> float:
        return 1.0 if occurrence["polarity"] == "BULLISH_DIVERGENCE" else -1.0

    def compile(
        self,
        occurrences: list[dict[str, Any]],
        reference_states: list[dict[str, Any]],
        role_paths: list[dict[str, Any]],
        selected_task_ids: tuple[str, ...] = (),
    ) -> tuple[list[CompiledLabel], dict[str, dict[str, int]]]:
        selected = set(selected_task_ids)
        path_index = self._path_index(role_paths)
        state_index = self._state_index(reference_states)
        data_end = max((x["observed_at_ms"] for x in role_paths), default=0)
        out: list[CompiledLabel] = []
        stats: dict[str, dict[str, int]] = {}
        for task in self.tasks:
            task_id = task["task_id"]
            if selected and task_id not in selected:
                continue
            stats[task_id] = {"mature": 0, "unmature": 0, "missing": 0, "neutral": 0}
            contract_id = task["label_contract_id"]
            contract = self.labels[contract_id]
            for occurrence in occurrences:
                cut = int(occurrence["observation_cut_ms"])
                kind = str(task["kind"])
                target: float | None = None
                censor_event = 0
                censor_duration_ms = 0
                maturity = cut
                role = contract.get("evaluation_symbol_role")
                state = state_index.get((occurrence["family"], occurrence["reference_cycle_id"], occurrence["level_side"]))
                horizon_policy = contract.get("horizon_policy")
                horizon_seconds = contract.get("horizon_seconds")
                if horizon_policy == "FIXED_SECONDS":
                    maturity = cut + int(horizon_seconds) * 1000
                elif horizon_policy == "ACTIVE_CYCLE_END":
                    role_probe = path_index.get((occurrence["event_id"], role or "HUNTER"), [])
                    maturity = int(role_probe[0]["active_cycle_end_ms"]) if role_probe else cut
                elif contract_id == "rthp.label.time_to_reference_exhaustion":
                    maturity = data_end
                if maturity > data_end and contract_id != "rthp.label.time_to_reference_exhaustion":
                    stats[task_id]["unmature"] += 1
                    continue
                if contract_id.startswith("rthp.label.reference_exhausted_") or contract_id == "rthp.label.reference_exhausted_by_active_cycle_end":
                    exhaustion_known = None if state is None else state.get("exhaustion_known_time_ms")
                    target = 1.0 if exhaustion_known is not None and int(exhaustion_known) <= maturity else 0.0
                elif contract_id == "rthp.label.time_to_reference_exhaustion":
                    exhaustion_known = None if state is None else state.get("exhaustion_known_time_ms")
                    if exhaustion_known is not None:
                        censor_event = 1
                        censor_duration_ms = max(0, int(exhaustion_known) - cut)
                    else:
                        censor_event = 0
                        censor_duration_ms = max(0, data_end - cut)
                    target = float(censor_event)
                else:
                    if role not in ("HUNTER", "PROTECTED"):
                        stats[task_id]["missing"] += 1
                        continue
                    path = path_index.get((occurrence["event_id"], role), [])
                    if not path:
                        stats[task_id]["missing"] += 1
                        continue
                    start_price = self._price_at(path, cut, known_by_ms=maturity)
                    end_price = self._price_at(path, maturity, known_by_ms=maturity)
                    if start_price is None or end_price is None or start_price <= 0 or end_price <= 0:
                        stats[task_id]["missing"] += 1
                        continue
                    signed_return = self._sign(occurrence) * math.log(end_price / start_price)
                    if "polarity_signed_log_return" in contract_id:
                        target = signed_return
                    elif "polarity_aligned_direction" in contract_id:
                        if signed_return == 0.0:
                            stats[task_id]["neutral"] += 1
                            continue
                        target = 1.0 if signed_return > 0 else 0.0
                    elif "_mfe_" in contract_id or "_mae_" in contract_id:
                        window = self._window(path, cut, maturity, known_by_ms=maturity)
                        if not window:
                            stats[task_id]["missing"] += 1
                            continue
                        signed: list[float] = []
                        for point in window:
                            candidates = (point.get("low"), point.get("high")) if point.get("low") is not None and point.get("high") is not None else (point.get("price"),)
                            for candidate_price in candidates:
                                price = float(candidate_price)
                                if price > 0:
                                    signed.append(self._sign(occurrence) * math.log(price / start_price))
                        if not signed:
                            stats[task_id]["missing"] += 1
                            continue
                        target = max(signed) if "_mfe_" in contract_id else max(-x for x in signed)
                    else:
                        target = signed_return
                if target is None or not math.isfinite(target):
                    stats[task_id]["missing"] += 1
                    continue
                ranking_group = f"{occurrence['trading_day_ny']}:{occurrence['level_side']}"
                out.append(CompiledLabel(
                    occurrence["event_id"], task_id, contract_id, kind, float(target), maturity,
                    maturity, ranking_group, censor_event, censor_duration_ms,
                ))
                stats[task_id]["mature"] += 1
        return out, stats
