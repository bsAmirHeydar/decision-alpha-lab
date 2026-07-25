import pytest
from strategy_factory_tournament_v3.folds import build_walk_forward_folds,assert_no_overlap
from strategy_factory_tournament_v3.ledger import TournamentLedger
from strategy_factory_tournament_v3.enums import Stage
from strategy_factory_tournament_v3.contracts import LedgerEntry
from strategy_factory_tournament_v3.errors import TournamentError
@pytest.mark.parametrize('count',[1,2,3,4,5])
def test_fold_generation(count):
 folds=build_walk_forward_folds(0,1000,count,1,1);assert len(folds)==count;assert assert_no_overlap(folds)
@pytest.mark.parametrize('count',[0,-1])
def test_bad_fold_count(count):
 with pytest.raises(TournamentError):build_walk_forward_folds(0,1000,count)
def test_ledger_chain():
 l=TournamentLedger();a=l.append(Stage.INVENTORY,'inventory',{'x':1},1);b=l.append(Stage.FREEZE,'freeze',{'x':2},2);assert b.previous_hash==a.entry_hash;assert l.verify()
def test_ledger_tamper_detected():
 l=TournamentLedger();a=l.append(Stage.INVENTORY,'inventory',{'x':1},1)
 bad=LedgerEntry(a.entry_id,a.sequence,a.stage,a.event_type,a.payload_hash,'1'*64,a.timestamp_ms,a.actor_id)
 with pytest.raises(TournamentError):TournamentLedger((bad,))
