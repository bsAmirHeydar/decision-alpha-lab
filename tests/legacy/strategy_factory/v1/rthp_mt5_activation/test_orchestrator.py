import json
from pathlib import Path
from strategy_factory_rthp_mt5_activation_v1.config import load_mt5_activation_config
from strategy_factory_rthp_mt5_activation_v1.orchestrator import RTHPMT5Automation
from strategy_factory_rthp_mt5_activation_v1.verify import verify_mt5_run

def test_one_click_source_run_is_idempotent(config_path,fake_provider,repo_root):
    c=load_mt5_activation_config(config_path); first=RTHPMT5Automation(c,fake_provider,repo_root).run(); second=RTHPMT5Automation(c,fake_provider,repo_root).run()
    assert first['status']=='PASS' and second['run_digest']==first['run_digest']; assert verify_mt5_run(c.output_root)['status']=='PASS'

def test_one_click_with_train_delegates_existing_pipeline(config_path,fake_provider,repo_root):
    raw=json.loads(config_path.read_text()); raw['output_root']=(Path(raw['output_root']).parent/'trained').as_posix(); raw['train']['enabled']=True; raw['train']['selected_task_ids']=['rthp.hunter.polarity_signed_log_return.15m']; raw['train']['minimum_mature_rows']=8; config_path.write_text(json.dumps(raw))
    result=RTHPMT5Automation(load_mt5_activation_config(config_path),fake_provider,repo_root).run(); assert result['status']=='PASS'; assert result['train_status'] in {'PASS','PASS_WITH_SKIPS'}
