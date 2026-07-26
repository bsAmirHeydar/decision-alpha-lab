#!/usr/bin/env python3
from __future__ import annotations
import csv, json, sys
from pathlib import Path

EXPECTED_PHASES = {f"P{i:02d}" for i in range(21)}

def validate(repo: Path) -> list[str]:
    errors=[]
    base=repo/'docs/operations/execution/EXP0018_daye_trader_intermarket_divergence/implementation_design_v2'
    reg_path=base/'data/EXP0018_IMPLEMENTATION_PHASE_REGISTRY_V2.json'
    if not reg_path.exists(): return [f"missing {reg_path}"]
    reg=json.loads(reg_path.read_text(encoding='utf-8'))
    phases=reg.get('phases',[])
    ids=[p['id'] for p in phases]
    if set(ids)!=EXPECTED_PHASES: errors.append(f"phase IDs mismatch: {ids}")
    if len(ids)!=len(set(ids)): errors.append('duplicate phase IDs')
    tracks={p['id']:p['track'] for p in phases}
    for p in phases:
        for d in p.get('deps',[]):
            if d not in tracks: errors.append(f"unknown dependency {d} -> {p['id']}")
            if p['track']=='core' and tracks.get(d)=='optional': errors.append(f"core phase {p['id']} depends on optional {d}")
    core=[p for p in phases if p['track']=='core']
    opt=[p for p in phases if p['track']=='optional']
    if len(core)!=14: errors.append(f"expected 14 core phases, got {len(core)}")
    if len(opt)!=7: errors.append(f"expected 7 optional phases, got {len(opt)}")
    for p in phases:
        pattern=f"PHASE{p['num']}_*_DESIGN_PACKET.md"
        folder=base/('02_core_track' if p['track']=='core' else '03_enrichment_track')
        if len(list(folder.glob(pattern)))!=1: errors.append(f"phase packet missing/duplicate for {p['id']}")
    dec=base/'data/EXP0018_DECISION_GATE_REGISTRY_V2.csv'
    if not dec.exists(): errors.append('decision registry missing')
    else:
        rows=list(csv.DictReader(dec.open(encoding='utf-8-sig')))
        if len(rows)<12: errors.append('decision registry too small')
        for r in rows:
            if not r.get('decision_id') or not r.get('blocked_phases'): errors.append(f"bad decision row {r}")
    for moc in [
        'CG_EXP0018_IMPLEMENTATION_DESIGN_V2_MOC.md','CG_EXP0018_CORE_IMPLEMENTATION_MOC.md',
        'CG_EXP0018_ENRICHMENT_IMPLEMENTATION_MOC.md','CG_EXP0018_ARCHITECTURE_CONTRACTS_MOC.md','CG_EXP0018_QA_RELEASE_MOC.md']:
        if not (repo/'docs/history/obsidian/deep/00_mocs'/moc).exists(): errors.append(f"missing MOC {moc}")
    return errors

def main() -> int:
    repo=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    errors=validate(repo)
    if errors:
        print('EXP0018 implementation design v2 validation: FAIL')
        for e in errors: print('ERROR:',e)
        return 1
    print('EXP0018 implementation design v2 validation: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
