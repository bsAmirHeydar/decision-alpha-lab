import pytest
from strategy_factory_tournament_v3.golden import golden_run
from strategy_factory_tournament_v3.contexts import adapt_exp0017,adapt_hook_zone,causal_replay
from strategy_factory_tournament_v3.inventory import validate_occurrences,future_suffix_invariant,validate_inventory
from strategy_factory_tournament_v3.errors import TournamentError
BASE=golden_run();INV=BASE[0];EXP,HZ=BASE[1]
EXP_RAW={'direction':'short','divergence_gap':2.0,'hunter_displacement':3.0,'clean_displacement':1.0,'group_minutes':60,'event_time_ms':2000,'known_time_ms':2100,'symbol_scope':['US100','US500'],'source_ids':['x']}
HZ_RAW={'direction':'long','hook_phase':'f2','f_count':2,'rally_count':1,'zone_width_atr':1.0,'zone_freshness':'fresh','structure_grade':'A','confirmation_state':'closed','setup_id':'hook_zone.personal.setup_alpha','event_time_ms':3000,'known_time_ms':3100,'symbol_scope':['SYMBOL'],'source_ids':['h']}
@pytest.mark.parametrize('missing',['direction','divergence_gap','hunter_displacement','clean_displacement','group_minutes'])
def test_exp0017_required(missing):
 raw=dict(EXP_RAW);raw.pop(missing)
 with pytest.raises(TournamentError):adapt_exp0017(raw,EXP)
@pytest.mark.parametrize('missing',['direction','hook_phase','f_count','rally_count','zone_width_atr','zone_freshness','structure_grade','confirmation_state','setup_id'])
def test_hook_zone_required(missing):
 raw=dict(HZ_RAW);raw.pop(missing)
 with pytest.raises(TournamentError):adapt_hook_zone(raw,HZ)
@pytest.mark.parametrize('freshness',['fresh','retested','consumed'])
def test_hook_zone_freshness_valid(freshness):
 raw=dict(HZ_RAW,zone_freshness=freshness)
 assert adapt_hook_zone(raw,HZ).features['hook_zone.zone_freshness']==freshness
@pytest.mark.parametrize('freshness',['future','unknown',''])
def test_hook_zone_freshness_invalid(freshness):
 with pytest.raises(TournamentError):adapt_hook_zone(dict(HZ_RAW,zone_freshness=freshness),HZ)
def test_forbidden_outcome_feature_rejected():
 raw=dict(EXP_RAW);raw['future_return']=9
 with pytest.raises(TournamentError):adapt_exp0017(raw,EXP)
def test_causal_replay_excludes_future():
 rows=[dict(EXP_RAW,known_time_ms=2100),dict(EXP_RAW,known_time_ms=5000,event_time_ms=4900,source_ids=['y'])]
 assert len(causal_replay(adapt_exp0017,EXP,rows,3000))==1
def test_inventory_validation_and_future_suffix():
 occ=list(BASE[2]);assert validate_occurrences(INV,occ)==tuple(sorted(occ,key=lambda x:(x.known_time_ms,x.occurrence_id)))
 assert future_suffix_invariant([occ[0]],[occ[1]],occ[0].known_time_ms)
 with pytest.raises(TournamentError):validate_inventory(INV,require_real=True)
