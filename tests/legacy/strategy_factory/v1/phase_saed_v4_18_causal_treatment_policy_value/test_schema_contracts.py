import importlib.util

def test_all_schema_pairs(load,root,art):
 spec=importlib.util.spec_from_file_location('_schema_validator',root/'src/engine/tooling/strategy_factory/saed_v4_18/_schema_validator.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 cmap=load(f'{art}/CONTRACT_VALIDATION_MAP.JSON')
 for row in cmap['contracts']:m.validate(load(row['document']),load(row['schema']))
 assert cmap['unknown_fields_forbidden'] and cmap['contract_count']==len(cmap['contracts'])
