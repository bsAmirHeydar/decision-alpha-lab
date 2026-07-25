from __future__ import annotations
from .canonical import content_hash,stable_id

def checkpoint_card(checkpoint,metrics,parity,probe,training_receipt):
    material={'checkpoint_id':checkpoint['checkpoint_id'],'checkpoint_hash':checkpoint['checkpoint_hash'],'candidate_id':checkpoint['candidate_id'],'architecture':checkpoint['architecture'],'validation_metrics':metrics['summary']['validation'],'test_metrics':metrics['summary']['test'],'streaming_parity_passed':parity['passed'],'state_collapsed':probe['collapsed'],'training_receipt_hash':training_receipt['receipt_hash'],'evidence_scope':'synthetic_reference','authority':'research_only','real_alpha_claimed':False,'runtime_authority':False}
    return {**material,'card_id':stable_id('sequencecard',material),'card_hash':content_hash(material)}
