from __future__ import annotations
from typing import Any
from .errors import BudgetError
from .canonical import with_digest
class ResourceAccountant:
    def __init__(self,budget:dict[str,Any]): self.budget=budget; self.tasks=0; self.cpu=0; self.peak_memory=0; self.bytes=0; self.objects=0
    def charge(self,task:dict,output_bytes:int,objects:int=1)->dict:
        self.tasks+=1; self.cpu+=task['budget']['cpu_seconds']; self.peak_memory=max(self.peak_memory,task['budget']['memory_mb']); self.bytes+=output_bytes; self.objects+=objects
        checks={'tasks':self.tasks<=self.budget['max_tasks'],'cpu':self.cpu<=self.budget['max_cpu_seconds'],'memory':self.peak_memory<=self.budget['max_memory_mb'],'bytes':self.bytes<=self.budget['max_store_bytes'],'objects':self.objects<=self.budget['max_store_objects']}
        if not all(checks.values()): raise BudgetError(str([k for k,v in checks.items() if not v]))
        return checks
    def document(self)->dict:
        return with_digest({'schema_version':'1.0.0','budget_id':self.budget['budget_id'],'task_count_charged':self.tasks,'cpu_seconds_charged':self.cpu,'peak_memory_mb_charged':self.peak_memory,'output_bytes_charged':self.bytes,'object_count_charged':self.objects,'within_budget':True,'budget_expansion_allowed':False},'accounting_digest')
