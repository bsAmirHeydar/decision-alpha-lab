from strategy_factory_classical_v3 import *
def test_catalog_broad_and_unique():
 assert len(CATALOG)>=35;assert len({x.key for x in CATALOG})==len(CATALOG);assert {'baseline','linear','tree','boosting','kernel','neighborhood','probabilistic','additive','optional_external'}<={x.family.value for x in CATALOG}
def test_mandatory_algorithms_present():
 for x in ('never_trade','always_trade','prevalence','manual_threshold','single_feature_search','rate_matched_null','logistic_regression','decision_tree_classifier','random_forest_classifier'):assert x in BY_ID
def test_behavior_parameters_change_identity():
 from dataclasses import replace
 a=BY_ID['logistic_regression'];b=replace(a,default_hyperparameters={**a.default_hyperparameters,'C':2.0});assert a.descriptor_hash!=b.descriptor_hash
def test_snapshot_frozen_and_hashed():
 s=ClassicalAlgorithmRegistry().freeze().snapshot();assert s.frozen and s.evidence_hash and len(s.descriptors)==len(CATALOG)
