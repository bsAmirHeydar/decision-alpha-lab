import json,pytest
from strategy_factory_generation import *
def factory():return EnvelopeFactory('run_1','gen_1')
def event(f,i=1):return f.create(RecordType.ANATOMY_EVENT,f'e{i}','p','1.0.0',1000+i,1000+i,'schema/event',{'x':i})
def test_sequence_monotonic():
    f=factory();assert event(f).sequence==1 and event(f,2).sequence==2

def test_record_id_stable():
    f=factory();e=event(f);assert e.record_id==e.derived_id

def test_causality_rejected():
    with pytest.raises(ValueError):ResultEnvelope(1,RecordType.ANATOMY_EVENT,'r','g','a','p','1',2,1,'s','h',{})

def test_memory_sink_append_and_seal():
    f=factory();s=AppendOnlyMemorySink();s.write(event(f));s.seal();assert s.telemetry.records_written==1 and s.telemetry.sealed
    with pytest.raises(RuntimeError):s.write(event(f,2))

def test_memory_non_monotonic_rejected():
    f=factory();e1=event(f);e2=event(f,2);s=AppendOnlyMemorySink()
    with pytest.raises(ValueError):s.write(e2)

def test_jsonl_roundtrip(tmp_path):
    f=factory();p=tmp_path/'ledger.jsonl';s=JsonlResultSink(p);s.open();s.write(event(f));s.write(event(f,2));s.seal();rows=[json.loads(x) for x in p.read_text().splitlines()];assert [r['sequence'] for r in rows]==[1,2]


def test_jsonl_existing_ledger_rejected(tmp_path):
    p=tmp_path/'ledger.jsonl';p.write_text('{}\n')
    s=JsonlResultSink(p)
    with pytest.raises(FileExistsError):s.open()
