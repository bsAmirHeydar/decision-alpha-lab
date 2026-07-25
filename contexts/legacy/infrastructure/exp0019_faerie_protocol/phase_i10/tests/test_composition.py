import pytest
from fp_i10_indicator import *
from fp_i10_indicator.enums import ModuleStatus
from fp_i10_indicator.canonical import canonical_sha256
from fp_i10_indicator.errors import FPI10InitializationError

def test_exact_composition(config,modules):
 c=build_composition(config,modules); assert tuple(m.phase_id for m in c.modules)==EXPECTED_UPSTREAM_PHASES

def test_version_mismatch_blocks(config,modules):
 bad=list(modules); m=bad[0]; bad[0]=UpstreamModuleDescriptor(m.phase_id,'9.9.9',m.contract_hash,'NONE',m.status,())
 with pytest.raises(FPI10InitializationError): build_composition(config,tuple(bad))
def test_sequence_mismatch_blocks(config,modules):
 with pytest.raises(FPI10InitializationError): build_composition(config,tuple(reversed(modules)))
def test_blocked_upstream_blocks(config,modules):
 bad=list(modules); m=bad[2]; bad[2]=UpstreamModuleDescriptor(m.phase_id,m.version,m.contract_hash,'NONE',ModuleStatus.BLOCKED,('X',))
 with pytest.raises(FPI10InitializationError): build_composition(config,tuple(bad))
def test_manifest_hash_changes_with_contract(config,modules):
 c1=build_composition(config,modules); bad=list(modules); m=bad[-1]; bad[-1]=UpstreamModuleDescriptor(m.phase_id,m.version,canonical_sha256({'changed':1}),'NONE',m.status,())
 c2=build_composition(config,tuple(bad)); assert c1.manifest_hash!=c2.manifest_hash
