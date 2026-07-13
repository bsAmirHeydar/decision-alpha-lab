from __future__ import annotations
from .contracts import MigrationUnit,MigrationWavePlan
from .enums import MigrationWave,MigrationStatus
from .canonical import canonical_sha256,stable_id
CATALOG={
 MigrationWave.A:(('temporal_intermarket_divergence','intermarket'),('exp0017_family','intermarket')),
 MigrationWave.B:(('nds','structural'),('hook','structural'),('f_counting','structural'),('rally','structural'),('zone','structural'),('structural_nodes','structural')),
 MigrationWave.C:(('daye_cycle','cycle'),('ict_deterministic','ict'),('astro_features','astro'),('manual_only_setups','manual_only')),
}
def build_wave(wave:MigrationWave,core_snapshot_hash:str,stop_after_unit:str|None=None)->MigrationWavePlan:
    units=[]
    for context_id,family in CATALOG[wave]:
        seed={'context_id':context_id,'wave':wave.value,'family':family}
        units.append(MigrationUnit(stable_id('migration-unit',seed),context_id,wave,canonical_sha256({'adapter':seed}),canonical_sha256({'spec':seed}),family,canonical_sha256({'capabilities':seed}),MigrationStatus.PARITY_PENDING,(),('real_data_parity_required',)))
    return MigrationWavePlan(stable_id('wave-plan',{'wave':wave.value,'units':[u.unit_id for u in units],'stop':stop_after_unit}),'1.0.0',wave,tuple(units),stop_after_unit,core_snapshot_hash)
