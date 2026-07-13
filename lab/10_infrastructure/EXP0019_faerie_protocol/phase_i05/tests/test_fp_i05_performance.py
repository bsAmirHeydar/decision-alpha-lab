from fp_i05_reference.benchmark import run_calendar_depth_benchmark

def test_calendar_depth_366_is_bounded():
    report=run_calendar_depth_benchmark(366,20)
    assert report['selection_count']==7320
    assert report['elapsed_seconds']<2.0
