from strategy_factory_rthp_context_v1 import RTHPContextPackage, build_auxiliary_payload, cluster_dimensions
from strategy_factory_contexts_v3 import RepresentationViewRegistry, ClusterCompiler, RepresentationKind
from helpers import records

def sequence_aux(package,frame,source):
 aux=dict(build_auxiliary_payload(source)); windows={}
 for d in package.view_descriptors():
  if d.kind is RepresentationKind.SEQUENCE:
   vm={v.feature_id:v.value for v in frame.values}
   for fid in d.feature_ids: windows[fid]=[vm[fid]]*d.shape[1]
 aux['sequence_windows']=windows
 return aux

def test_all_registered_views_compile_deterministically():
 p=RTHPContextPackage(); vr=RepresentationViewRegistry(); row=records()[0]; obs=p.observe(row)[0]; frame=p.build_feature_frame(obs,row); aux=sequence_aux(p,frame,row)
 hashes=[]
 for d in p.view_descriptors(): hashes.append(vr.compile(d,frame,aux).view_hash)
 hashes2=[vr.compile(d,frame,aux).view_hash for d in p.view_descriptors()]
 assert len(hashes)==5 and hashes==hashes2 and len(set(hashes))==5

def test_intermarket_view_uses_roles_not_raw_symbol_ids():
 p=RTHPContextPackage(); vr=RepresentationViewRegistry(); row=records()[0]; obs=p.observe(row)[0]; frame=p.build_feature_frame(obs,row); aux=sequence_aux(p,frame,row)
 d=next(x for x in p.view_descriptors() if x.kind is RepresentationKind.INTERMARKET)
 payload=vr.compile(d,frame,aux).payload
 assert payload['symbols']==['HUNTER_ROLE','PROTECTED_ROLE']
 assert row['primary_symbol'] not in str(payload) and row['secondary_symbol'] not in str(payload)

def test_cluster_assignments_are_deterministic_and_distinct_by_rule():
 p=RTHPContextPackage(); cc=ClusterCompiler(); row=records()[0]; obs=p.observe(row)[0]; dims=cluster_dimensions(row,label_horizon_group='60m')
 a=[cc.compile(r,obs,dims) for r in p.cluster_rules()]; b=[cc.compile(r,obs,dims) for r in p.cluster_rules()]
 assert [x.cluster_id for x in a]==[x.cluster_id for x in b]
 assert len({x.cluster_id for x in a})==4

def test_same_reference_cluster_groups_related_occurrences():
 p=RTHPContextPackage(); cc=ClusterCompiler(); a=records()[0]; b=dict(a); b['event_id']='RTHPEVT_'+'F'*32; b['active_cycle_id']='ACTIVE_DIFFERENT'; b['source_content_hash']='sha256:'+'f'*64; b['auxiliary']=build_auxiliary_payload(b)
 rule=next(x for x in p.cluster_rules() if x.rule_id=='rthp.reference.v1')
 ca=cc.compile(rule,p.observe(a)[0],cluster_dimensions(a)).cluster_id
 cb=cc.compile(rule,p.observe(b)[0],cluster_dimensions(b)).cluster_id
 assert ca==cb

def test_opportunity_cluster_separates_active_cycle_siblings():
 p=RTHPContextPackage(); cc=ClusterCompiler(); a=records()[0]; b=dict(a); b['event_id']='RTHPEVT_'+'E'*32; b['active_cycle_id']='ACTIVE_DIFFERENT'; b['source_content_hash']='sha256:'+'e'*64; b['auxiliary']=build_auxiliary_payload(b)
 rule=next(x for x in p.cluster_rules() if x.rule_id=='rthp.opportunity.v1')
 assert cc.compile(rule,p.observe(a)[0],cluster_dimensions(a)).cluster_id != cc.compile(rule,p.observe(b)[0],cluster_dimensions(b)).cluster_id
