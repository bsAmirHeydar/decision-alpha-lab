import copy,pytest
from saed_v4_context_twin.service import ContextTwinService
from saed_v4_context_twin.registry import TwinRegistry
from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.errors import RegistryError

def test_service_initialize(context_spec,seed):
 s=ContextTwinService();m=s.initialize(context_spec,seed);snap=s.snapshot(m.twin_id,m.exact_version,'2026-07-13T10:00:00Z');assert snap.twin_id==m.twin_id
def test_registry_idempotent(context_spec,seed):
 r=TwinRegistry();m=compile_twin(context_spec,seed);r.register(m);r.register(m);assert r.get(m.twin_id,m.exact_version)==m
def test_registry_rebind(context_spec,seed):
 r=TwinRegistry();m=compile_twin(context_spec,seed);r.register(m);bad=type(m)(**{**m.__dict__,'semantic_hash':'0'*64})
 with pytest.raises(RegistryError):r.register(bad)
