import json
from pathlib import Path
from strategy_factory_rthp_mt5_activation_v1.config import load_mt5_activation_config
from strategy_factory_rthp_mt5_activation_v1.orchestrator import RTHPMT5Automation
from strategy_factory_rthp_train_activation_v1.config import load_activation_config
from strategy_factory_rthp_train_activation_v1.m1_materializer import RTHPM1HistoricalMaterializer

def test_m1_materializer_never_synthesizes_ticks(config_path,fake_provider,tmp_path,repo_root):
    raw=json.loads(config_path.read_text()); raw['train']['enabled']=False; config_path.write_text(json.dumps(raw))
    result=RTHPMT5Automation(load_mt5_activation_config(config_path),fake_provider,repo_root).run(); run=Path(raw['output_root'])
    p=run/'source/primary_m1.jsonl'; s=run/'source/secondary_m1.jsonl'; train={'schema_version':'1.0.0','run_id':'M1_TEST','output_root':(tmp_path/'train').as_posix(),'data_source':{'mode':'PAIRED_M1_BAR_JSONL','provider':'Fake','primary_symbol':'FAKE_A','secondary_symbol':'FAKE_B','primary_m1_bar_jsonl':p.as_posix(),'secondary_m1_bar_jsonl':s.as_posix(),'timezone':'America/New_York','price_basis':'BID','tick_size_source':'FAKE','contract_roll_policy':'NONE','entitlement_id':'TEST','producer_version':'TEST','availability_time_policy':'M1_BAR_CLOSE_UTC_MS','source_revision':'R1','start_time_ms':None,'end_time_ms':None,'max_confirmation_freshness_ms':0},'split_policy':{'minimum_mature_rows':8,'oof_train_fraction':.2,'oof_calibration_fraction':.05,'oof_threshold_fraction':.05,'oof_holdout_fraction':.1,'final_train_fraction':.35,'final_calibration_fraction':.05,'final_threshold_fraction':.05,'final_test_fraction':.15,'purge_ms':0,'embargo_ms':0},'resource_policy':{'seed':1,'max_rows':100000,'max_features':10000,'max_memory_mb':1024,'max_wall_seconds':120,'max_workers':1},'selected_task_ids':[],'family_filter':['M15_CYCLE_GROUP'],'train_all_mature_tasks':True,'retain_materialized_views':True,'fail_on_task_insufficiency':False}
    tp=tmp_path/'train.json'; tp.write_text(json.dumps(train)); mat=RTHPM1HistoricalMaterializer(load_activation_config(tp)).materialize(tmp_path/'mat')
    report=json.loads(mat.materialization_report.read_text()); assert report['synthetic_ticks_created'] is False; assert report['intrabar_order_inferred'] is False; assert mat.occurrence_count>0
    occurrences=[json.loads(line) for line in mat.occurrence_ledger.read_text().splitlines() if line.strip()]
    paths=[json.loads(line) for line in mat.role_price_path_ledger.read_text().splitlines() if line.strip()]
    cuts={row['event_id']:row['observation_cut_ms'] for row in occurrences}
    grouped={}
    for row in paths: grouped.setdefault((row['event_id'],row['evaluation_symbol_role']),[]).append(row)
    assert grouped
    for (event_id,role),rows in grouped.items():
        assert min(row['observed_at_ms'] for row in rows) <= cuts[event_id], (event_id,role)
        assert all(row['intrabar_order']=='UNKNOWN' for row in rows)

