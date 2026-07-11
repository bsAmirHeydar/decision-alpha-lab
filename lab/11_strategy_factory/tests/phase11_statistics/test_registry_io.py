from strategy_factory_statistics.registry import default_metric_registry,MetricRegistry,MetricDescriptor
from strategy_factory_statistics.io import read_samples_csv
from pathlib import Path
import pytest

def test_default_registry_stable():
    a=default_metric_registry();b=default_metric_registry();assert a.registry_hash==b.registry_hash and len(a.items)>=8
def test_duplicate_metric_rejected():
    x=MetricDescriptor('x','1','R','mean',1)
    with pytest.raises(ValueError):MetricRegistry([x,x])
def test_example_csv_loads():
    p=Path(__file__).resolve().parents[2]/'examples'/'phase11'/'statistical_samples.csv'
    rows=read_samples_csv(p);assert len(rows)==24 and rows[0].sample_id=='sample_000'
