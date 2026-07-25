from fp_i14_diagnostic import *
def test_indicator_ea_pass(runs): assert compare_runs(runs[ProductKind.INDICATOR],runs[ProductKind.DIAGNOSTIC_EA]).status==DifferentialStatus.PASS
def test_indicator_python_pass(runs): assert compare_runs(runs[ProductKind.INDICATOR],runs[ProductKind.PYTHON_REFERENCE]).status==DifferentialStatus.PASS
def test_ea_python_pass(runs): assert compare_runs(runs[ProductKind.DIAGNOSTIC_EA],runs[ProductKind.PYTHON_REFERENCE]).status==DifferentialStatus.PASS
def test_cross_product_pass(runs): assert compare_products(tuple(runs.values())).status==DifferentialStatus.PASS
def test_missing_product_blocks(runs): assert compare_products((runs[ProductKind.INDICATOR],runs[ProductKind.DIAGNOSTIC_EA])).status==DifferentialStatus.BLOCKED
