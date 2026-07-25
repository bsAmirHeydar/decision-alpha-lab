from __future__ import annotations
from .canonical import content_hash, stable_id
from .errors import BudgetError

def build_compute_budget(max_pairs:int,max_epochs:int,max_dimension:int,max_wall_seconds:float=30.0)->dict:
    if min(max_pairs,max_epochs,max_dimension)<=0 or max_wall_seconds<=0: raise BudgetError('invalid compute budget')
    payload={"phase":"SAED_V4_11","max_training_pairs":max_pairs,"max_epochs":max_epochs,"max_embedding_dimension":max_dimension,"max_wall_seconds":float(max_wall_seconds),"gpu_required":False,"external_network_allowed":False,"budget_scope":"reference_synthetic"}
    payload['budget_id']=stable_id('computebudget',payload);payload['budget_hash']=content_hash(payload);return payload

def assert_budget(config,budget):
    epochs=sum(x.epochs for x in config.curriculum)
    if config.max_total_pairs>budget['max_training_pairs']: raise BudgetError('pair budget exceeded by config')
    if epochs>budget['max_epochs']: raise BudgetError('epoch budget exceeded by config')
    if config.embedding_dim>budget['max_embedding_dimension']: raise BudgetError('dimension budget exceeded by config')
