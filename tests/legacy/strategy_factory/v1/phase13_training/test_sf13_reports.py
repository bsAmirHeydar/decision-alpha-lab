from strategy_factory_training.examples import build_reference_training_bundle
from strategy_factory_training import write_training_bundle

def test_report_bundle_is_machine_readable(tmp_path):
    dataset,label,plan,trained=build_reference_training_bundle();paths=write_training_bundle(tmp_path,trained,dataset.manifest,plan)
    assert len(paths)==8 and (tmp_path/"predictions.csv").read_text().count("\n")==len(trained.predictions)+1
