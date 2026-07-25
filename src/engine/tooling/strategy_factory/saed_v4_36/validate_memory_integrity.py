from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__);m=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_36/GOLDEN_MEMORY.JSON').read_text());n=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_36/GOLDEN_NEGATIVE_KNOWLEDGE.JSON').read_text());r=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_36/GOLDEN_RETRIEVAL_RECEIPT.JSON').read_text())
assert m['append_only'] and m['semantic_duplicates']==0 and len(m['merkle_root'])==64
assert m['chain'][0]['previous_hash']=='0'*64 and all(m['chain'][i]['previous_hash']==m['chain'][i-1]['event_hash'] for i in range(1,len(m['chain'])))
assert n['record_count']>=4 and n['deletion_allowed'] is False
assert any(q['negative_recall_count']>0 for q in r['queries'])
print('V4-36 memory integrity passed')
