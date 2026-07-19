import shutil,pytest
from tools.strategy_factory.lcm.lcm_05.verify import verify_package
from tools.strategy_factory.lcm.lcm_05.errors import IntegrityError

def test_package_verifies(topology_root):assert verify_package(topology_root)['passed']
def test_tamper_detected(topology_root,tmp_path):
    d=tmp_path/'p';shutil.copytree(topology_root,d);p=d/'reports/topology_summary.json';p.write_text(p.read_text()+'\n')
    with pytest.raises(IntegrityError):verify_package(d)
