from fp_i11_visual import *

def test_runtime_authority_none(): assert runtime_authority()=='NONE'
def test_visual_authority_only(): assert visual_authority()=='CHART_OBJECTS_ONLY'
def test_forbidden_scan(): assert 'OrderSend' in scan_text('void x(){ OrderSend(); }')
def test_clean_scan(): assert scan_text('ObjectCreate chart only')==()
