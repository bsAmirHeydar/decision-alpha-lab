from tools.repository_paths import find_repository_root
import json
from pathlib import Path
from saed_v4_constitution.canonical import content_hash
from saed_v4_constitution.conformance import run_vector
from saed_v4_constitution.policy import ConstitutionKernel,ConstitutionPolicy
from saed_v4_constitution.replay import replay_authority
from saed_v4_constitution.models import AuthorityRequest
from saed_v4_constitution.enums import Authority

ROOT=find_repository_root(__file__)

def test_default_policy_healthy(constitution_hash): assert ConstitutionKernel(constitution_hash).health()['status']=='allow'

def test_dangerous_policy_unhealthy(constitution_hash):
 p=ConstitutionPolicy('x','4.0.0',True,1,90,True,True,True,True,('reject',)); assert ConstitutionKernel(constitution_hash,p).health()['status']=='reject'

def test_replay_sorted_and_deterministic(kernel,agent):
 a=AuthorityRequest('p',agent,Authority.RESEARCH_PROPOSAL,'2026-07-13T00:02:00Z','x')
 b=AuthorityRequest('p',agent,Authority.SANDBOX_COMPUTE,'2026-07-13T00:01:00Z','x')
 x=replay_authority(kernel,[a,b]); y=replay_authority(kernel,[b,a]); assert [i.decision_id for i in x]==[i.decision_id for i in y]

def test_all_conformance_vectors(constitution_doc):
 vectors=json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_00/constitutional_conformance_vectors.json').read_text())['vectors']
 k=ConstitutionKernel(content_hash(constitution_doc)); results=[run_vector(k,v) for v in vectors]; assert all(x['matches_expected'] for x in results)
