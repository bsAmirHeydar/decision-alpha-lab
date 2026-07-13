import pytest
from dataclasses import replace
from strategy_factory_tournament_v3.treatments import default_treatment_universe
from strategy_factory_tournament_v3.algorithms import default_algorithm_universe
from strategy_factory_tournament_v3.enums import TreatmentFamily,AlgorithmFamily
from strategy_factory_tournament_v3.errors import TournamentError

def test_all_treatment_families_frozen():
 u=default_treatment_universe(1,2);assert {x.family for x in u.treatments}==set(TreatmentFamily);assert len(u.treatments)==9

def test_all_algorithm_families_frozen():
 u=default_algorithm_universe(1,2,True);assert {x.family for x in u.algorithms}==set(AlgorithmFamily);assert len(u.algorithms)==9
@pytest.mark.parametrize('idx',range(9))
def test_treatment_hash_deterministic(idx):
 a=default_treatment_universe(1,2);b=default_treatment_universe(1,2);assert a.treatments[idx].spec_hash==b.treatments[idx].spec_hash
@pytest.mark.parametrize('idx',range(9))
def test_algorithm_hash_deterministic(idx):
 a=default_algorithm_universe(1,2,True);b=default_algorithm_universe(1,2,True);assert a.algorithms[idx].spec_hash==b.algorithms[idx].spec_hash

def test_deep_unqualified_fails_closed():
 with pytest.raises(TournamentError):default_algorithm_universe(1,2,False)

def test_mutation_changes_universe_hash():
 a=default_treatment_universe(1,2);row=replace(a.treatments[0],max_loss_r=2.0);b=replace(a,treatments=(row,)+a.treatments[1:]);assert a.universe_hash!=b.universe_hash
