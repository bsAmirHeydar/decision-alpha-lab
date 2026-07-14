import argparse,json
from pathlib import Path
from .composition import descriptors_from_repository
from .inputs import build_config
from .engine import IndicatorEngine
from .enums import DataReadiness,ActiveWWDirection
from .diagnostics import build_diagnostic
from .canonical import canonicalize

def main():
 p=argparse.ArgumentParser(); p.add_argument('repo'); p.add_argument('--primary',default='ES'); p.add_argument('--secondary',default='NQ'); p.add_argument('--epoch',default='FP-EPOCH-1'); a=p.parse_args()
 modules=descriptors_from_repository(Path(a.repo)); cfg=build_config(context_epoch=a.epoch,primary_symbol=a.primary,secondary_symbol=a.secondary)
 eng=IndicatorEngine(); now=1783900800000; eng.initialize(config=cfg,chart_id=1,terminal_instance_id='CLI-TERMINAL',modules=modules,now_m1=now)
 state={'data_readiness':DataReadiness.READY,'history_ready':True,'source_revision_id':'REV-CLI','source_revision_sequence':1,'active_ww_direction':ActiveWWDirection.NONE,'confirmed_signal_count':0,'allowed_signal_count':0,'suppressed_by_ww_count':0,'suppressed_by_quota_count':0,'quota_winner_signal_id':'','ledger_event_count':0}
 eng.timer(now_m1=now,upstream_state=state); print(json.dumps(canonicalize(build_diagnostic(eng,now)),indent=2))
if __name__=='__main__': main()
