from __future__ import annotations
import argparse,json
from pathlib import Path
def validate_jsonl(path:Path)->dict:
    last=0;ids=set();count=0
    with path.open(encoding='utf-8') as f:
        for line in f:
            row=json.loads(line);seq=int(row['sequence'])
            if seq!=last+1:raise ValueError(f'non-monotonic sequence {seq}')
            if row['record_id'] in ids:raise ValueError('duplicate record_id')
            ids.add(row['record_id']);last=seq;count+=1
    return {'records':count,'last_sequence':last,'unique_ids':len(ids)}
def main():
    p=argparse.ArgumentParser();p.add_argument('ledger',type=Path);a=p.parse_args();print(json.dumps(validate_jsonl(a.ledger),indent=2))
if __name__=='__main__':main()
