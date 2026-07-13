from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'mql5/Include/FaerieProtocol/EXP0019/Compatibility'

def test_required_mql5_contract_files_exist():
    names={'FP_I01_Enums.mqh','FP_I01_Types.mqh','FP_I01_Fingerprint.mqh','FP_I01_DependencyPins.mqh','FP_I01_CGAdapters.mqh','FP_I01_DAYEAdapters.mqh','FP_I01_Registry.mqh','FP_I01_SelfTest.mqh','FP_I01_All.mqh'}
    assert names=={p.name for p in BASE.glob('*.mqh')}

def test_mql5_registry_has_eight_adapters_and_no_authority():
    text=(BASE/'FP_I01_Registry.mqh').read_text()
    assert 'return 8;' in text and text.count('case ')==8
    assert 'order_authority=false' in text and 'broker_authority=false' in text and 'network_authority=false' in text

def test_adapters_take_const_source_references():
    text=(BASE/'FP_I01_CGAdapters.mqh').read_text()+(BASE/'FP_I01_DAYEAdapters.mqh').read_text()
    assert text.count('const ')>=8
    assert 'OrderSend' not in text and 'CTrade' not in text and 'WebRequest' not in text

def test_includes_resolve_case_sensitively():
    for p in BASE.glob('*.mqh'):
        for line in p.read_text().splitlines():
            if '#include "' in line:
                name=line.split('"')[1]
                assert (BASE/name).exists(),(p,name)
