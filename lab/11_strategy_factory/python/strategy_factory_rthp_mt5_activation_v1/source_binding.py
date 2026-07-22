from __future__ import annotations
from pathlib import Path
from .canonical import sha256_file,sha256_material,write_json,write_jsonl

def freeze_source(root: Path, terminal_receipt, primary, secondary, quality, acquisition_receipts, revision: str):
    source=root/'source'; ppath=source/'primary_m1.jsonl'; spath=source/'secondary_m1.jsonl'
    write_jsonl(ppath,[x.to_dict() for x in quality.primary_bars]); write_jsonl(spath,[x.to_dict() for x in quality.secondary_bars])
    write_json(source/'terminal_receipt.json',terminal_receipt); write_json(source/'primary_symbol_metadata.json',primary.metadata|{'metadata_digest':primary.metadata_digest})
    write_json(source/'secondary_symbol_metadata.json',secondary.metadata|{'metadata_digest':secondary.metadata_digest})
    write_json(source/'acquisition_receipts.json',{'receipts':list(acquisition_receipts)}); write_json(source/'quality_report.json',quality.report)
    binding={'schema_version':'1.0.0','binding_id':'RTHP_MT5_M1_SOURCE_BINDING','status':'FROZEN','canonical_source_timeframe':'M1_CLOSED_BARS',
             'sub_m1_source_allowed':False,'synthetic_ticks_created':False,'common_range':{'start_ms':quality.common_start_ms,'end_ms':quality.common_end_ms},
             'sources':[{'role':'PRIMARY','symbol':primary.broker_symbol,'artifact_uri':ppath.resolve().as_uri(),'content_hash':'sha256:'+sha256_file(ppath)},
                        {'role':'SECONDARY','symbol':secondary.broker_symbol,'artifact_uri':spath.resolve().as_uri(),'content_hash':'sha256:'+sha256_file(spath)}],
             'terminal_id':terminal_receipt['terminal_id'],'source_revision':revision,'quality_report_digest':quality.report['report_digest']}
    binding['binding_digest']=sha256_material(binding); write_json(source/'mt5_m1_source_binding.json',binding)
    return ppath,spath,binding
