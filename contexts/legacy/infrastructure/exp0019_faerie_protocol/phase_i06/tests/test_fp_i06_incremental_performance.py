from fp_i02_kernel.enums import RelationCode,PriceSide
from fp_i06_relations.golden import golden_store_and_report
from fp_i06_relations.conformance import _row
from fp_i06_relations.engine import scan_side_plan,cursor_from_result
from fp_i06_relations.enums import ScanMode
from fp_i06_relations.benchmark import benchmark_scan

def fixture_rows(count=120):
    *_,report,_=golden_store_and_report(1);p=next(x for x in report.side_plans if x.relation is RelationCode.AL and x.side is PriceSide.HIGH);rows=[]
    for i in range(count):rows.append(_row(p,p.check_start_utc_ms+i*60_000,p.left_reference_price-1,p.left_reference_price-2,p.right_reference_price-1,p.right_reference_price-2,i*2))
    rows[-1]=_row(p,rows[-1].open_utc_ms,p.left_reference_price+.1,p.left_reference_price-2,p.right_reference_price-1,p.right_reference_price-2,999)
    return p,tuple(rows)
def test_batch_scan_is_deterministic_and_linear_counted():
    p,rows=fixture_rows();r=scan_side_plan(p,rows,'REV',ScanMode.BATCH)
    assert r.processed_row_count==len(rows) and r.candidate is not None
def test_cursor_points_to_first_unprocessed_minute():
    p,rows=fixture_rows(10);r=scan_side_plan(p,rows,'REV');c=cursor_from_result(r)
    assert c.next_open_utc_ms==rows[-1].open_utc_ms+60_000
def test_benchmark_reports_bounded_scan():
    p,rows=fixture_rows();b=benchmark_scan(p,rows,'REV',2)
    assert b['row_count']==120 and b['maximum_ms']<1000
