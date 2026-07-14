from fp_i12_operator import *
import pytest
def test_checkpoint_valid(config):
 a=AlertRouter(config.instance_id,config.alerts).snapshot();cp=build_checkpoint(config,default_preferences(config),a,sha256('s'));assert validate_checkpoint(cp,config)
def test_checkpoint_config_mismatch(config):
 a=AlertRouter(config.instance_id,config.alerts).snapshot();cp=build_checkpoint(config,default_preferences(config),a,sha256('s'));bad=OperatorConfig('INSTANCE-1','FP19::INSTANCE-1::',PanelConfig(mode=PanelMode.AUDIT),FilterConfig(),config.alerts,config.export,'UNSET');
 with pytest.raises(FPI12Error):validate_checkpoint(cp,bad)
def test_checkpoint_corruption(config):
 a=AlertRouter(config.instance_id,config.alerts).snapshot();cp=build_checkpoint(config,default_preferences(config),a,sha256('s'));bad=OperatorCheckpoint(cp.checkpoint_id,cp.version,cp.instance_id,cp.config_hash,cp.preferences,cp.alert_state,cp.last_snapshot_hash,sha256('bad'));
 with pytest.raises(FPI12Error):validate_checkpoint(bad,config)
