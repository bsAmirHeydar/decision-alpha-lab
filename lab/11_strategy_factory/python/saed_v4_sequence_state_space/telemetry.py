from __future__ import annotations
from .canonical import content_hash,stable_id

def telemetry(sequence_manifest,tournament,registry,parity_docs):
    material={'phase':'SAED_V4_12','sequence_count':sequence_manifest['sequence_count'],'candidate_count':len(tournament['rows']),'admitted_reference_count':registry['admitted_count'],'parity_pass_count':sum(x['passed'] for x in parity_docs),'parity_fail_count':sum(not x['passed'] for x in parity_docs),'reference_champion_id':tournament['reference_champion_id'],'runtime_activation':False,'alerts':[]}
    return {**material,'telemetry_id':stable_id('seqtelemetry',material),'telemetry_hash':content_hash(material)}
