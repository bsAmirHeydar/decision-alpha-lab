from __future__ import annotations
from .contracts import ContextOccurrence,ContextPackageFreeze,DataInventory
from .canonical import canonical_sha256,stable_id
from .errors import TournamentError

def _feature_policy(features:dict,allowed:tuple[str,...],forbidden:tuple[str,...]):
 unknown=set(features)-set(allowed)
 leak=set(features)&set(forbidden)
 if leak:raise TournamentError('exploitation_leakage_feature','forbidden feature present',{'features':sorted(leak)})
 if unknown:raise TournamentError('unknown_context_feature','feature not declared',{'features':sorted(unknown)})

def adapt_exp0017(raw:dict,freeze:ContextPackageFreeze)->ContextOccurrence:
 if {'future_return','outcome_label','future_path'} & set(raw):raise TournamentError('exploitation_leakage_feature','future/outcome field present in raw context')
 required={'direction','divergence_gap','hunter_displacement','clean_displacement','group_minutes'}
 missing=required-set(raw)
 if missing:raise TournamentError('exp0017_missing_fields','missing exp0017 fields',{'fields':sorted(missing)})
 features={f'exp0017.{k}':raw[k] for k in required}
 _feature_policy(features,freeze.allowed_feature_ids,freeze.forbidden_feature_ids)
 event=int(raw['event_time_ms']);known=int(raw['known_time_ms'])
 return ContextOccurrence(stable_id('uce15_exp0017',raw),freeze.context_id,freeze.context_version,known,event,tuple(raw.get('symbol_scope',('US100','US500'))),features,str(raw.get('lifecycle_state','confirmed')),tuple(raw.get('source_ids',('exp0017.source',))),bool(raw.get('matured',True)))

def adapt_hook_zone(raw:dict,freeze:ContextPackageFreeze)->ContextOccurrence:
 if {'future_return','outcome_label','future_path'} & set(raw):raise TournamentError('exploitation_leakage_feature','future/outcome field present in raw context')
 required={'direction','hook_phase','f_count','rally_count','zone_width_atr','zone_freshness','structure_grade','confirmation_state','setup_id'}
 missing=required-set(raw)
 if missing:raise TournamentError('hook_zone_missing_fields','missing hook/zone fields',{'fields':sorted(missing)})
 if raw['zone_freshness'] not in ('fresh','retested','consumed'):raise TournamentError('invalid_zone_freshness','zone freshness invalid')
 if int(raw['f_count'])<0 or int(raw['rally_count'])<0:raise TournamentError('invalid_structure_count','structure counts non-negative')
 features={f'hook_zone.{k}':raw[k] for k in required}
 _feature_policy(features,freeze.allowed_feature_ids,freeze.forbidden_feature_ids)
 event=int(raw['event_time_ms']);known=int(raw['known_time_ms'])
 return ContextOccurrence(stable_id('uce15_hook_zone',raw),freeze.context_id,freeze.context_version,known,event,tuple(raw.get('symbol_scope',('SYMBOL',))),features,str(raw.get('lifecycle_state','confirmed')),tuple(raw.get('source_ids',('hook_zone.source',))),bool(raw.get('matured',True)))

def causal_replay(adapter,freeze:ContextPackageFreeze,rows:list[dict],cut_ms:int)->tuple[ContextOccurrence,...]:
 out=[]
 for raw in sorted(rows,key=lambda x:(int(x['known_time_ms']),str(x.get('source_ids','')))):
  if int(raw['known_time_ms'])<=cut_ms:out.append(adapter(raw,freeze))
 return tuple(out)
