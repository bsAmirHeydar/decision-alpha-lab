from fp_i10_indicator.health import *
from fp_i10_indicator.enums import *

def build(modules,now,status=ModuleStatus.READY):
 return tuple(build_module_health(m,now,'REV',0) for m in modules)
def test_ready_health(config,modules):
 h=aggregate_health(lifecycle=LifecycleState.READY,data_readiness=DataReadiness.READY,history_ready=True,checkpoint_disposition=CheckpointDisposition.RESTORED,module_health=build(modules,60000),incremental_lag_minutes=0,last_processing_duration_us=1,generated_utc_ms=60000,config_hash=config.config_hash); assert h.overall is HealthState.READY
def test_history_degrades(config,modules):
 h=aggregate_health(lifecycle=LifecycleState.READY,data_readiness=DataReadiness.READY,history_ready=False,checkpoint_disposition=CheckpointDisposition.ABSENT,module_health=build(modules,60000),incremental_lag_minutes=0,last_processing_duration_us=1,generated_utc_ms=60000,config_hash=config.config_hash); assert h.overall is HealthState.DEGRADED
def test_data_blocks(config,modules):
 h=aggregate_health(lifecycle=LifecycleState.READY,data_readiness=DataReadiness.BLOCKED,history_ready=True,checkpoint_disposition=CheckpointDisposition.RESTORED,module_health=build(modules,60000),incremental_lag_minutes=0,last_processing_duration_us=1,generated_utc_ms=60000,config_hash=config.config_hash); assert h.overall is HealthState.BLOCKED
def test_lag_degrades(config,modules):
 h=aggregate_health(lifecycle=LifecycleState.READY,data_readiness=DataReadiness.READY,history_ready=True,checkpoint_disposition=CheckpointDisposition.RESTORED,module_health=build(modules,60000),incremental_lag_minutes=5,last_processing_duration_us=1,generated_utc_ms=60000,config_hash=config.config_hash); assert h.overall is HealthState.DEGRADED
