from __future__ import annotations
from .contracts import AlgorithmSpec,AlgorithmUniverseFreeze
from .enums import AlgorithmFamily

def default_algorithm_universe(declared_at_ms:int,outcome_cut_ms:int,deep_qualified:bool=True)->AlgorithmUniverseFreeze:
 rows=(
 AlgorithmSpec('uce15.algorithm.manual','1.0.0',AlgorithmFamily.MANUAL,'binary',('tabular',),0,1,True),
 AlgorithmSpec('uce15.algorithm.naive_frequency','1.0.0',AlgorithmFamily.NAIVE,'binary',('tabular',),1,1,True),
 AlgorithmSpec('uce15.algorithm.logistic','1.0.0',AlgorithmFamily.CLASSICAL,'binary',('tabular',),11,4,True),
 AlgorithmSpec('uce15.algorithm.random_forest','1.0.0',AlgorithmFamily.CLASSICAL,'binary',('tabular',),12,6,True),
 AlgorithmSpec('uce15.algorithm.rank_pairwise','1.0.0',AlgorithmFamily.RANKING,'ranking',('tabular','intermarket'),21,5,True),
 AlgorithmSpec('uce15.algorithm.treatment_choice','1.0.0',AlgorithmFamily.TREATMENT_CHOICE,'multiclass',('tabular','treatment'),31,8,True),
 AlgorithmSpec('uce15.algorithm.survival_aft','1.0.0',AlgorithmFamily.SURVIVAL,'survival',('tabular','path'),41,8,True),
 AlgorithmSpec('uce15.algorithm.distributional_quantiles','1.0.0',AlgorithmFamily.DISTRIBUTIONAL,'distributional',('tabular','path'),51,8,True),
 AlgorithmSpec('uce15.algorithm.deep_multiview','1.0.0',AlgorithmFamily.DEEP,'binary',('tabular','sequence','graph'),61,12,deep_qualified,{'torch':deep_qualified}))
 return AlgorithmUniverseFreeze('uce15.algorithm_universe','1.0.0',declared_at_ms,outcome_cut_ms,rows,True)
