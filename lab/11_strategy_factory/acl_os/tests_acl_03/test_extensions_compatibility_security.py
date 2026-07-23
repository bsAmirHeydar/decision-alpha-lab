import copy,os
import pytest
from tools.strategy_factory.acl_os.acl_03.compatibility import validate_compatibility
from tools.strategy_factory.acl_os.acl_03.extensions import resolve_extensions
from tools.strategy_factory.acl_os.acl_03.detector_ir import compile_detector_ir
from tools.strategy_factory.acl_os.acl_03.known_time_ir import compile_known_time_ir
from tools.strategy_factory.acl_os.acl_03.feature_binding_ir import compile_feature_binding_ir
from tools.strategy_factory.acl_os.acl_03.adapters import compile_adapter_contracts
from tools.strategy_factory.acl_os.acl_03.security import evaluate_security_boundary
from tools.strategy_factory.acl_os.acl_03.source_snapshot import build_source_snapshot
from tools.strategy_factory.acl_os.acl_03.service import COMPILER_VERSION

def test_compatibility_passes(package): assert validate_compatibility(package,COMPILER_VERSION)['compatible']
@pytest.mark.parametrize('version',['2.0.0','0.9.0','bad'])
def test_context_schema_major_fails(package,version):
    p=copy.deepcopy(package);p['manifest']['schema_version']=version;assert not validate_compatibility(p,COMPILER_VERSION)['compatible']
def test_empty_extensions_pass(package): assert resolve_extensions(package)['passed']
@pytest.mark.parametrize('kind',['EXECUTION_ADAPTER','CAPITAL_ALLOCATOR','SHELL_PLUGIN','MODEL_TRAINER'])
def test_forbidden_extension_kind(package,kind):
    p=copy.deepcopy(package);p['manifest']['extensions']=[{'extension_id':'X','extension_kind':kind,'capabilities':[],'public_ports_only':True}];r=resolve_extensions(p);assert not r['passed']
@pytest.mark.parametrize('cap',['ORDER_SUBMISSION','CAPITAL_ACCESS','UNBOUNDED_NETWORK','UNBOUNDED_FILESYSTEM','DYNAMIC_CODE_EXECUTION','AUTHORITY_ESCALATION'])
def test_forbidden_extension_capability(package,cap):
    p=copy.deepcopy(package);p['manifest']['extensions']=[{'extension_id':'X','extension_kind':'DOMAIN_LINTER','capabilities':[cap],'public_ports_only':True}];assert not resolve_extensions(p)['passed']
def test_security_boundary_passes(context_root,package):
    d,_=compile_detector_ir(package);k,_=compile_known_time_ir(package);f,_=compile_feature_binding_ir(package);a=compile_adapter_contracts(package,k,f);assert evaluate_security_boundary(context_root,package,d,a)['passed']
@pytest.mark.skipif(not hasattr(os,'symlink'),reason='symlink unavailable')
def test_source_snapshot_rejects_symlink(tmp_path,context_root,package):
    # Isolated minimal copy proves traversal rejects symlinks. Windows may
    # require Developer Mode or an elevated token; that host capability is not
    # evidence that the production guard is absent.
    import shutil
    dst=tmp_path/'ctx';shutil.copytree(context_root,dst)
    try:
        os.symlink(dst/'README.md',dst/'linked.md',target_is_directory=False)
    except OSError as exc:
        if os.name=='nt' and getattr(exc,'winerror',None)==1314:
            pytest.skip('Windows symlink privilege is unavailable on this host')
        raise
    with pytest.raises(ValueError):build_source_snapshot(dst,package,COMPILER_VERSION)
