#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_data_foundation.content_store import ContentAddressedStore
from saed_v4_data_foundation.integrity import build_integrity_receipt
out=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_01_generated';out.mkdir(parents=True,exist_ok=True);store=ContentAddressedStore(out/'cas');digest=store.put_text('SAED-V4-01-reference');receipt=build_integrity_receipt(digest,{'reference':digest});(out/'content_receipt.json').write_text(json.dumps(receipt.__dict__,indent=2),encoding='utf-8');print(json.dumps({'status':'pass','content_hash':digest,'receipt_id':receipt.receipt_id},indent=2))
