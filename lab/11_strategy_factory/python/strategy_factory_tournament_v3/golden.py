from __future__ import annotations
from .canonical import canonical_sha256
from .contracts import *
from .enums import *
from .contexts import adapt_exp0017,adapt_hook_zone
from .treatments import default_treatment_universe
from .algorithms import default_algorithm_universe
from .folds import build_walk_forward_folds
from .tournament import run_reference_tournament
from .prospective import build_paper_report
from .decision import decide_champion

def golden_inventory():
 return DataInventory('uce15.inventory.reference','1.0.0','uce15.reference_fixture',canonical_sha256({'rows':12}),DataMode.FIXTURE,12,('US100','US500','SYMBOL'),1000,12000,'known_time_ms','repo://lab/11_strategy_factory/examples/uce_i15',12000,canonical_sha256({'schema':'uce15.reference'}),('reference fixture only','not market-edge evidence'))
def golden_context_freezes(inv):
 exp=ContextPackageFreeze('uce15.freeze.exp0017','1.0.0','ucee.reference.exp0017','1.0.0',*[canonical_sha256({'x':x}) for x in ('doctrine','features','cluster','lifecycle','known')],('exp0017.direction','exp0017.divergence_gap','exp0017.hunter_displacement','exp0017.clean_displacement','exp0017.group_minutes'),('exp0017.future_return','exp0017.outcome_label'),('exp0017.manual_divergence_baseline',),inv.inventory_hash)
 hz=ContextPackageFreeze('uce15.freeze.hook_zone','1.0.0','ucee.reference.hook_zone','1.0.0',*[canonical_sha256({'hz':x}) for x in ('doctrine','features','cluster','lifecycle','known')],('hook_zone.direction','hook_zone.hook_phase','hook_zone.f_count','hook_zone.rally_count','hook_zone.zone_width_atr','hook_zone.zone_freshness','hook_zone.structure_grade','hook_zone.confirmation_state','hook_zone.setup_id'),('hook_zone.future_return','hook_zone.outcome_label'),('hook_zone.personal.setup_alpha',),inv.inventory_hash)
 return exp,hz
def golden_occurrences(exp,hz):
 e=adapt_exp0017({'direction':'short','divergence_gap':24.0,'hunter_displacement':25.0,'clean_displacement':1.0,'group_minutes':60,'event_time_ms':2000,'known_time_ms':2100,'symbol_scope':['US100','US500'],'source_ids':['exp17.1']},exp)
 h=adapt_hook_zone({'direction':'long','hook_phase':'f2_retest','f_count':2,'rally_count':1,'zone_width_atr':0.8,'zone_freshness':'fresh','structure_grade':'A','confirmation_state':'closed','setup_id':'hook_zone.personal.setup_alpha','event_time_ms':3000,'known_time_ms':3100,'symbol_scope':['SYMBOL'],'source_ids':['hz.1']},hz)
 return (e,h)
def golden_run():
 inv=golden_inventory();exp,hz=golden_context_freezes(inv);occ=golden_occurrences(exp,hz);t=default_treatment_universe(500,1000);a=default_algorithm_universe(500,1000,True);folds=build_walk_forward_folds(1000,12000,3,1,1)
 freeze=TournamentFreeze('uce15.reference_tournament','1.0.0',inv.inventory_hash,(exp.freeze_hash,hz.freeze_hash),t.universe_hash,a.universe_hash,folds,('mean_net_r','sharpe','max_drawdown_r','calibration_error'),('causality','multiplicity','prospective','parity','risk'),3,17,10000,True)
 report=run_reference_tournament(freeze,(exp.context_id,hz.context_id),t,a)
 plan=ProspectivePaperPlan('uce15.paper_plan','1.0.0','1'*64,13000,23000,20,False,False,'2'*64,0.05,('decision_hash','expected_entry','observed_entry','expected_cost','observed_cost'))
 paper=build_paper_report(plan,(),DataMode.FIXTURE,False,True)
 decision=decide_champion(report,paper,None)
 return inv,(exp,hz),occ,t,a,freeze,report,plan,paper,decision
