from pathlib import Path
import importlib.util

def test_all_schema_pairs(load,root):
 spec=importlib.util.spec_from_file_location('_schema_validator',root/'tools/strategy_factory/saed_v4_17/_schema_validator.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 cmap=load('lab/11_strategy_factory/artifacts/saed_v4_17/CONTRACT_VALIDATION_MAP.JSON')
 for row in cmap['contracts']:m.validate(load(row['document']),load(row['schema']))
def test_closed_contract_map(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_17/CONTRACT_VALIDATION_MAP.JSON');assert x['closed_contracts'] and x['unknown_fields_forbidden'] and x['contract_count']>=45
