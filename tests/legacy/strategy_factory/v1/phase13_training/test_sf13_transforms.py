from strategy_factory_training.examples import build_reference_training_bundle
from strategy_factory_training import *

def test_transform_fits_training_only():
    bundle=build_reference_training_bundle()[0];spec=TransformSpec();train=rows_for_role(bundle.rows,DatasetRole.TRAIN)
    state=fit_transform_state(train,bundle.columns,bundle.manifest.feature_schema_hash,spec);assert state.fitted_role==DatasetRole.TRAIN
    try:fit_transform_state(train+(rows_for_role(bundle.rows,DatasetRole.TEST)[0],),bundle.columns,bundle.manifest.feature_schema_hash,spec);assert False
    except ValueError:pass

def test_transform_is_deterministic():
    bundle=build_reference_training_bundle()[0];spec=TransformSpec();train=rows_for_role(bundle.rows,DatasetRole.TRAIN)
    a=fit_transform_state(train,bundle.columns,bundle.manifest.feature_schema_hash,spec);b=fit_transform_state(train,bundle.columns,bundle.manifest.feature_schema_hash,spec)
    assert a.transform_hash==b.transform_hash
