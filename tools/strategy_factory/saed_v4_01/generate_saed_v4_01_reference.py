#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_data_foundation.content_store import ContentAddressedStore
from saed_v4_data_foundation.integrity import build_integrity_receipt
out=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_01_generated';out.mkdir(parents=True,exist_ok=True);store=ContentAddressedStore(out/'cas');digest=store.put_text('SAED-V4-01-reference');receipt=build_integrity_receipt(digest,{'reference':digest});(out/'content_receipt.json').write_text(json.dumps(receipt.__dict__,indent=2),encoding='utf-8');print(json.dumps({'status':'pass','content_hash':digest,'receipt_id':receipt.receipt_id},indent=2))
