from tools.strategy_factory.lcm.lcm_15c.io import file_digest
def test_empty_pathspec(package_root):p=package_root/'final_deletion_pathspec.txt';assert p.read_bytes()==b'' and file_digest(p)=='sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
