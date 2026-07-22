from datetime import datetime,timezone
from strategy_factory_rthp_mt5_activation_v1.acquire import acquire_symbol,resolve_range
from strategy_factory_rthp_mt5_activation_v1.config import load_mt5_activation_config
from strategy_factory_rthp_mt5_activation_v1.quality import validate_pair
from strategy_factory_rthp_mt5_activation_v1.source_binding import freeze_source
from strategy_factory_rthp_mt5_activation_v1.symbols import resolve_symbol
from strategy_factory_rthp_mt5_activation_v1.terminal import TerminalSession
from dataclasses import asdict

def test_quality_and_immutable_binding(config_path,fake_provider,tmp_path):
    c=load_mt5_activation_config(config_path)
    with TerminalSession(fake_provider,None,1000,False,True) as session:
        p=resolve_symbol(fake_provider,c.primary_symbol,c.canonical_primary_id); s=resolve_symbol(fake_provider,c.secondary_symbol,c.canonical_secondary_id); start,end=resolve_range(fake_provider,p,s,c.history,datetime.now(timezone.utc))
        pa=acquire_symbol(fake_provider,p,start,end,c.history,session.receipt.terminal_id,c.source_revision); sa=acquire_symbol(fake_provider,s,start,end,c.history,session.receipt.terminal_id,c.source_revision)
        q=validate_pair(pa,sa,c.quality,c.history.minimum_common_days); pp,sp,b=freeze_source(tmp_path,asdict(session.receipt),p,s,q,(*pa.receipts,*sa.receipts),c.source_revision)
    assert q.status=='PASS'; assert b['status']=='FROZEN'; assert pp.is_file() and sp.is_file(); assert b['sub_m1_source_allowed'] is False
