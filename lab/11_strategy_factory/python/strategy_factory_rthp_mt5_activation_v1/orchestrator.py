from __future__ import annotations
import json,os,shutil
from dataclasses import asdict
from datetime import datetime,timezone
from pathlib import Path
from typing import Any
from strategy_factory_rthp_train_activation_v1.config import load_activation_config
from strategy_factory_rthp_train_activation_v1.pipeline import RTHPTrainActivationPipeline,verify_run_root
from .acquire import acquire_symbol,resolve_range
from .canonical import sha256_file,sha256_material,write_json
from .config import MT5ActivationConfig
from .provider import MetaTrader5Provider,MT5Provider
from .quality import validate_pair
from .source_binding import freeze_source
from .symbols import resolve_symbol
from .terminal import TerminalSession
from .verify import verify_mt5_run

class RTHPMT5Automation:
    def __init__(self,config:MT5ActivationConfig,provider:MT5Provider|None=None,repository_root:Path|None=None):
        self.config=config; self.provider=provider or MetaTrader5Provider(); self.repo=(repository_root or self._repo()).resolve()
    def _repo(self):
        p=Path(__file__).resolve()
        for c in (p,*p.parents):
            if (c/'lab/11_strategy_factory').is_dir() and (c/'registry').is_dir(): return c
        raise RuntimeError('repository root not found')
    def _hash_ledger(self,root):
        out=root/'MT5_RUN_FILE_HASHES.sha256'; rows=[]
        for p in sorted(root.rglob('*')):
            if p.is_file() and p!=out: rows.append(f"sha256:{sha256_file(p)}  {p.relative_to(root).as_posix()}\n")
        out.write_text(''.join(rows),encoding='utf-8',newline='\n')
    def _train_config(self,staging,ppath,spath,run_id):
        train_root=staging/'train_run'; raw={'schema_version':'1.0.0','run_id':run_id,'output_root':train_root.as_posix(),
          'data_source':{'mode':'PAIRED_M1_BAR_JSONL','provider':'MetaTrader5','primary_symbol':self.config.primary_symbol,'secondary_symbol':self.config.secondary_symbol,
                         'primary_m1_bar_jsonl':ppath.as_posix(),'secondary_m1_bar_jsonl':spath.as_posix(),'timezone':'America/New_York','price_basis':'BID',
                         'tick_size_source':'MT5_SYMBOL_TRADE_TICK_SIZE','contract_roll_policy':self.config.contract_roll_policy,'entitlement_id':self.config.entitlement_id,
                         'producer_version':'strategy_factory_rthp_mt5_activation_v1@1.0.0','availability_time_policy':'M1_BAR_CLOSE_UTC_MS',
                         'source_revision':self.config.source_revision,'start_time_ms':None,'end_time_ms':None,'max_confirmation_freshness_ms':0},
          'split_policy':{'minimum_mature_rows':self.config.train.minimum_mature_rows,'oof_train_fraction':0.20,'oof_calibration_fraction':0.05,
                          'oof_threshold_fraction':0.05,'oof_holdout_fraction':0.10,'final_train_fraction':0.35,'final_calibration_fraction':0.05,
                          'final_threshold_fraction':0.05,'final_test_fraction':0.15,'purge_ms':3600000,'embargo_ms':3600000},
          'resource_policy':{'seed':self.config.train.seed,'max_rows':self.config.train.max_rows,'max_features':10000,'max_memory_mb':self.config.train.max_memory_mb,
                             'max_wall_seconds':self.config.train.max_wall_seconds,'max_workers':1},'selected_task_ids':list(self.config.train.selected_task_ids),
          'family_filter':list(self.config.train.family_filter),'train_all_mature_tasks':not bool(self.config.train.selected_task_ids),
          'retain_materialized_views':True,'fail_on_task_insufficiency':False}
        path=staging/'resolved_train_activation.json'; write_json(path,raw); return path,train_root
    def preflight(self):
        with TerminalSession(self.provider,self.config.terminal.path,self.config.terminal.timeout_ms,self.config.terminal.portable,self.config.terminal.require_connected) as session:
            p=resolve_symbol(self.provider,self.config.primary_symbol,self.config.canonical_primary_id); s=resolve_symbol(self.provider,self.config.secondary_symbol,self.config.canonical_secondary_id)
            start,end=resolve_range(self.provider,p,s,self.config.history,datetime.now(timezone.utc))
            return {'status':'PASS','terminal':asdict(session.receipt),'primary_symbol':p.metadata,'secondary_symbol':s.metadata,'resolved_start_utc':start.isoformat(),
                    'resolved_end_utc':end.isoformat(),'canonical_source_timeframe':'M1_CLOSED_BARS','sub_m1_requested':False,'trading_authority_created':False}
    def run(self):
        final=self.config.output_root.resolve()
        if final.exists():
            v=verify_mt5_run(final)
            if v['status']=='PASS': return json.loads((final/'mt5_run_manifest.json').read_text(encoding='utf-8'))
            raise FileExistsError(f'incomplete or invalid output exists: {final}')
        staging=final.parent/f'.{final.name}.mt5_staging.{os.getpid()}'; shutil.rmtree(staging,ignore_errors=True); staging.mkdir(parents=True)
        try:
            write_json(staging/'activation_config.normalized.json',asdict(self.config))
            with TerminalSession(self.provider,self.config.terminal.path,self.config.terminal.timeout_ms,self.config.terminal.portable,self.config.terminal.require_connected) as session:
                p=resolve_symbol(self.provider,self.config.primary_symbol,self.config.canonical_primary_id); s=resolve_symbol(self.provider,self.config.secondary_symbol,self.config.canonical_secondary_id)
                start,end=resolve_range(self.provider,p,s,self.config.history,datetime.now(timezone.utc))
                pa=acquire_symbol(self.provider,p,start,end,self.config.history,session.receipt.terminal_id,self.config.source_revision)
                sa=acquire_symbol(self.provider,s,start,end,self.config.history,session.receipt.terminal_id,self.config.source_revision)
                quality=validate_pair(pa,sa,self.config.quality,self.config.history.minimum_common_days)
                if quality.status=='BLOCKED': raise RuntimeError('M1 source quality blocked: '+','.join(quality.report['blockers']))
                ppath,spath,binding=freeze_source(staging,asdict(session.receipt),p,s,quality,(*pa.receipts,*sa.receipts),self.config.source_revision)
            run_id=self.config.run_id if self.config.run_id!='AUTO' else f"RTHP_MT5_{p.broker_symbol}_{s.broker_symbol}_{binding['binding_digest'][:12].upper()}"
            train_report=None
            if self.config.train.enabled:
                config_path,train_root=self._train_config(staging,ppath,spath,run_id)
                train_report=RTHPTrainActivationPipeline(load_activation_config(config_path),self.repo).run()
                if verify_run_root(train_root)['status']!='PASS': raise RuntimeError('downstream train verification failed')
            manifest={'report_id':'RTHP_MT5_ONE_CLICK_ACTIVATION_V1','schema_version':'1.0.0','status':'PASS','run_id':run_id,
                      'primary_symbol':p.broker_symbol,'secondary_symbol':s.broker_symbol,'common_start_ms':quality.common_start_ms,'common_end_ms':quality.common_end_ms,
                      'canonical_source_timeframe':'M1_CLOSED_BARS','sub_m1_source_used':False,'synthetic_ticks_created':False,'intrabar_order_inferred':False,
                      'source_binding_digest':binding['binding_digest'],'quality_status':quality.status,'train_enabled':self.config.train.enabled,
                      'train_status':None if train_report is None else train_report['status'],'engine_modified':False,'canonical_context_modified':False,
                      'order_authority_created':False,'capital_authority_created':False}
            manifest['run_digest']=sha256_material(manifest); write_json(staging/'mt5_run_manifest.json',manifest)
            self._hash_ledger(staging); (staging/'MT5_RUN_COMPLETE').write_text(manifest['run_digest']+'\n',encoding='utf-8',newline='\n')
            staging.replace(final)
            if verify_mt5_run(final)['status']!='PASS': raise RuntimeError('MT5 run verification failed')
            return manifest
        except Exception:
            if staging.exists(): staging.replace(staging.with_name(staging.name+'.failed'))
            raise
