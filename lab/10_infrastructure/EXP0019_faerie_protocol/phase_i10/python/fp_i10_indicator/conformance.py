from .registry import contract_registry
from .channels import buffer_mapping
from .constants import BUFFER_COUNT,EXPECTED_UPSTREAM_PHASES

def run_conformance(engine):
    checks={
      'phase_registry':contract_registry()['phase_id']=='FP-I10',
      'module_sequence':tuple(m.phase_id for m in engine.composition.modules)==EXPECTED_UPSTREAM_PHASES,
      'buffer_count':len(engine.snapshot.buffers.values)==BUFFER_COUNT,
      'buffer_registry_count':len(buffer_mapping())==BUFFER_COUNT,
      'event_chain':engine.event_chain.validate(),
      'instance_namespace':engine.instance.object_namespace.startswith('FP19::'),
      'runtime_authority':contract_registry()['runtime_authority']=='NONE',
      'snapshot_config':engine.snapshot.health.config_hash==engine.config.config_hash,
    }
    return checks
