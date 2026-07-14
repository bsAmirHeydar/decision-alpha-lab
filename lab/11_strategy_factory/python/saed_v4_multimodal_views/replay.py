from .models import ViewReplayReceipt
from .errors import ReplayError
class ViewReplayer:
    def __init__(self,builder):self.builder=builder
    def replay(self,spec,request,expected_hash):
        observed=self.builder.build(spec,request)
        status='pass' if observed.view_hash==expected_hash else 'fail'
        receipt=ViewReplayReceipt(spec.specification_id,request.known_as_of,request.event_as_of,expected_hash,observed.view_hash,status)
        if status!='pass':raise ReplayError('view replay mismatch')
        return receipt
