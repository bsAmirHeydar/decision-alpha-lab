from fp_i14_diagnostic import *
def test_run_conformance(runs): assert all(validate_run(r) for r in runs.values())
def test_report_conformance(runs): assert validate_cross_product(compare_products(tuple(runs.values())))
def test_registry_contract_count(): assert len(registry()['public_contracts'])==13
def test_reason_codes_closed(): assert len(registry()['reason_codes'])==26 and len(set(registry()['reason_codes']))==26
