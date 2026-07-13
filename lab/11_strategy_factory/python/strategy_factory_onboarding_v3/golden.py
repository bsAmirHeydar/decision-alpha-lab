from __future__ import annotations
from pathlib import Path
from .canonical import canonical_sha256
from .contracts import *
from .capabilities import default_capabilities
from .generator import ContextGenerator
from .invariance import snapshot,compare
from .adapters import LegacyAdapter,measure_parity
from .waves import build_wave
from .migration import execute_wave
from .enums import *
def golden_spec()->ContextSpecification:
    features=(FeatureSpec('direction','category','known_at_close'),FeatureSpec('magnitude','float','known_at_close'),FeatureSpec('fresh','bool','known_at_close'))
    views=(ViewSpec('tabular',tuple(x.feature_id for x in features),(3,)),)
    return ContextSpecification('fixture.onboarded_context','1.0.0','Fixture Onboarded Context',ContextKind.STRUCTURAL,MigrationWave.B,canonical_sha256('doctrine'),(canonical_sha256('source'),),features,views,('forming','confirmed','retired'),('same_symbol_same_session',),('binary_direction','treatment_ranking'),'manual.fixture.v1',default_capabilities(),('legacy/fixture.py',),())
def golden_run(repo_root:Path):
    spec=golden_spec();before=snapshot(repo_root);gen=ContextGenerator();manifest,files,compiled=gen.build(spec,before);after=snapshot(repo_root);inv=compare(before,after)
    adapter_spec=LegacyAdapterSpec('fixture-adapter','1.0.0',spec.context_id,('legacy/fixture.py',),(canonical_sha256('source'),),AdapterMode.DIFFERENTIAL,True,True,True,True,True)
    fn=lambda p:{'direction':p['direction'],'magnitude':float(p['magnitude'])}
    adapter=LegacyAdapter(adapter_spec,fn,fn)
    obs=tuple(adapter.observe(f'obs-{i}',1000+i,{'direction':'up','magnitude':i/10}) for i in range(5))
    parity=measure_parity(adapter_spec,obs,0.0)
    wave=build_wave(MigrationWave.B,before.snapshot_hash,stop_after_unit=None)
    migration=execute_wave(wave,{u.unit_id:True for u in wave.units},('accepted_context',))
    return spec,before,manifest,files,compiled,inv,adapter_spec,parity,wave,migration
