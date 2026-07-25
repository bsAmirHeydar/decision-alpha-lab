from __future__ import annotations
import itertools
from .canonical import content_hash,stable_id

def domain_subset_matrix(domain_views,config):
    names=[x['view_name'] for x in domain_views];required=set(config.required_view_names);critical=set(config.critical_view_names);rows=[]
    for bits in itertools.product((0,1),repeat=len(names)):
        present={n for n,b in zip(names,bits) if b};mr=sorted(required-present);mc=sorted(critical-present);supported=not mr
        rows.append({'pattern_id':''.join(map(str,bits)),'present_count':len(present),'missing_count':len(names)-len(present),'missing_required':mr,'missing_critical':mc,'supported':supported,'directive':'fuse' if supported else 'abstain'})
    doc={'phase':'SAED_V4_15','view_names':names,'subset_count':len(rows),'expected_subset_count':2**len(names),'rows':rows,'all_subsets_bounded':all(r['directive'] in {'fuse','abstain'} for r in rows),'production_eligible':False};doc['matrix_hash']=content_hash(doc);doc['matrix_id']=stable_id('v415domainmatrix',doc);return doc

def foundation_subset_matrix(foundation_views):
    names=[x['view_name'] for x in foundation_views];rows=[]
    for bits in itertools.product((0,1),repeat=len(names)):
        c=sum(bits);rows.append({'pattern_id':''.join(map(str,bits)),'present_count':c,'missing_count':len(names)-c,'challenger_supported':c>=1,'directive':'challenger_eligible' if c>=1 else 'baseline_only'})
    doc={'phase':'SAED_V4_15','view_names':names,'subset_count':len(rows),'expected_subset_count':2**len(names),'rows':rows,'all_subsets_bounded':True,'production_eligible':False};doc['matrix_hash']=content_hash(doc);doc['matrix_id']=stable_id('v415foundationmatrix',doc);return doc

def dropout_plan(envelopes,config,policy):
    domain=[x for x in envelopes if x['source_plane']=='domain'];foundation=[x for x in envelopes if x['source_plane']=='foundation'];patterns=[]
    patterns.append({'name':'complete','drop_views':[],'expected_directive':'fuse'})
    for x in domain:
        patterns.append({'name':'drop_'+x['view_name'],'drop_views':[x['view_name']],'expected_directive':'abstain' if x['view_name'] in config.required_view_names else 'fuse'})
    for x in foundation: patterns.append({'name':'drop_'+x['view_name'],'drop_views':[x['view_name']],'expected_directive':'fuse'})
    groups={'drop_all_optional':list(config.optional_view_names),'drop_all_foundation':[x['view_name'] for x in foundation],'drop_execution_and_liquidity':['execution_view','liquidity_view'],'drop_time_stack':['time_view','session_view','higher_timeframe_view']}
    for n,vs in groups.items():patterns.append({'name':n,'drop_views':vs,'expected_directive':'abstain' if set(vs)&set(config.required_view_names) else 'fuse'})
    doc={'phase':'SAED_V4_15','dropout_rate':config.modality_dropout_rate,'structured_patterns':list(policy.structured_patterns),'patterns':patterns,'pattern_count':len(patterns),'outcome_conditioned':False,'production_eligible':False};doc['plan_hash']=content_hash(doc);doc['plan_id']=stable_id('v415dropout',doc);return doc
