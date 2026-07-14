from __future__ import annotations
import csv,json
from pathlib import Path
from .contracts import *
from .canonical import sha256,stable_id,primitive

class TraceExporter:
    def __init__(self): self.exported=set()
    def export(self,run:TraceRun,path,fmt:ExportFormat):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);app=dup=0
        records=[]
        for e in run.events:
            key=(run.product.value,e.computed_event_id,e.semantic_hash)
            if key in self.exported:dup+=1;continue
            self.exported.add(key);records.append(e);app+=1
        if fmt in (ExportFormat.JSONL,ExportFormat.BOTH):
            p=path if path.suffix=='.jsonl' else path.with_suffix('.jsonl')
            with p.open('a',encoding='utf-8') as f:
                for e in records: f.write(json.dumps(primitive(e), sort_keys=True) + '\n')
        if fmt in (ExportFormat.CSV,ExportFormat.BOTH):
            p=path if path.suffix=='.csv' else path.with_suffix('.csv');new=not p.exists()
            with p.open('a',encoding='utf-8',newline='') as f:
                wr=csv.writer(f)
                if new:wr.writerow(['product','sequence','event_type','semantic_id','payload_hash','state','relation','direction','source_revision_id','semantic_hash'])
                for e in records:wr.writerow([e.product.value,e.sequence,e.event_type.value,e.semantic_id,e.payload_hash,e.state,e.relation,e.direction,e.source_revision_id,e.semantic_hash])
        rid=stable_id('FPEXPREC',{'run':run.run_id,'format':fmt.value,'path':str(path),'appended':app,'duplicates':dup})
        return ExportReceipt(rid,fmt,str(path),app,dup,run.inventory.event_count,sha256({'receipt':rid,'run':run.run_hash}))
