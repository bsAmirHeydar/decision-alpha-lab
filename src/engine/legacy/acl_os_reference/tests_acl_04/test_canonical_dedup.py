from copy import deepcopy
from src.engine.tooling.strategy_factory.acl_os.acl_04.human_dsl import compile_human_setup
from src.engine.tooling.strategy_factory.acl_os.acl_04.candidate import build_candidate, behavior_payload
from src.engine.tooling.strategy_factory.acl_os.acl_04.deduplication import deduplicate
from src.engine.tooling.strategy_factory.acl_os.acl_04.canonical import digest_object


def make(ir,source):
    return build_candidate(ir,source_id=source,source_digest='sha256:'+'1'*64,authority_digest='sha256:'+'2'*64,envelope_digest='sha256:'+'3'*64,findings=[])


def test_origin_is_not_behavior_identity(fixtures):
    human=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    ai=deepcopy(human);ai['lane']='AI';ai['policy_ir_digest']=digest_object({k:v for k,v in ai.items() if k!='policy_ir_digest'})
    assert digest_object(behavior_payload(human))==digest_object(behavior_payload(ai))


def test_dedup_prefers_human(fixtures):
    human=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    ai=deepcopy(human);ai['lane']='AI';ai['policy_ir_digest']=digest_object({k:v for k,v in ai.items() if k!='policy_ir_digest'})
    canonical,report=deduplicate([make(ai,'AI_SOURCE'),make(human,'HUMAN_SOURCE')])
    assert len(canonical)==1
    assert canonical[0]['origin']=='HUMAN'
    assert report['groups'][0]['duplicate_count']==1
    assert report['groups'][0]['origins']==['AI','HUMAN']


def test_invalid_candidate_not_exported(fixtures):
    human=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    invalid=build_candidate(human,source_id='X_X',source_digest='sha256:'+'1'*64,authority_digest='sha256:'+'2'*64,envelope_digest='sha256:'+'3'*64,findings=[{'code':'X_X','severity':'BLOCKER','path':'x','details':{}}])
    canonical,report=deduplicate([invalid])
    assert canonical==[]
    assert report['canonical_count']==0
