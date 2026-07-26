from src.engine.tooling.strategy_factory.acl_os.acl_12.scanners import scan_secrets,scan_static,scan_mql5,scan_paths
def test_reference_secret_scan_passes(ACL11): assert scan_secrets(ACL11)['passed']
def test_secret_scanner_detects_key(tmp_path):
    (tmp_path/'x.txt').write_text('-----BEGIN PRIVATE KEY-----\nabc')
    assert not scan_secrets(tmp_path)['passed']
def test_static_scan_passes_acl11(ACL11): assert scan_static(ACL11)['passed']
def test_mql5_scan_passes_acl11(ACL11): assert scan_mql5(ACL11)['passed']
def test_symlink_scan(tmp_path):
    target=tmp_path/'a'; target.write_text('x'); link=tmp_path/'b'
    try: link.symlink_to(target)
    except OSError: return
    assert not scan_paths(tmp_path)['passed']
