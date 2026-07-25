from strategy_factory_statistics.models import StatisticalReportManifest,StatisticalSample
from strategy_factory_statistics.grouped import GroupedStatisticsEngine
from strategy_factory_statistics.confidence import normal_mean_interval
from strategy_factory_statistics.reports import ReportBundleWriter

def sample(i,r):return StatisticalSample(f's{i}',f'o{i}',f'c{i}',f'e{i}',f'cl{i}','st','EURUSD','long','ny',2026,7,4,'x',True,False,r,1,1,60)
def manifest():return StatisticalReportManifest('r','p','1','run','mh','ah','st','1','cm','sp','cr','gs','mr','nr',17,100,'abc').with_hash()
def test_report_bundle(tmp_path):
    s=GroupedStatisticsEngine().summarize([sample(1,1),sample(2,-.5)])[0]
    ci=normal_mean_interval('mean_net_r','all=all',s.mean_net_r,s.standard_deviation_r,s.filled_count)
    idx=ReportBundleWriter(tmp_path).write(manifest(),[s],[ci],[])
    assert (tmp_path/'report.md').exists() and (tmp_path/'artifact_index.json').exists() and len(idx.artifacts)==5
def test_report_bundle_deterministic_names(tmp_path):
    s=GroupedStatisticsEngine().summarize([sample(1,1)])[0]
    ReportBundleWriter(tmp_path).write(manifest(),[s],[],[])
    assert sorted(p.name for p in tmp_path.iterdir())==['artifact_index.json','confidence_intervals.csv','group_statistics.csv','matched_nulls.csv','report.md','report_manifest.json']
