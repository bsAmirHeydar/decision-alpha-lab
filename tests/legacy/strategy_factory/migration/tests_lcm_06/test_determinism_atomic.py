import tempfile,pytest
from pathlib import Path
from tools.strategy_factory.lcm.lcm_06.canonical import content_id
from tools.strategy_factory.lcm.lcm_06.io import atomic_publish
def test_content_id_deterministic(): assert content_id("X",{"b":2,"a":1})==content_id("X",{"a":1,"b":2})
def test_atomic_publish_refuses_existing(tmp_path):
    s=tmp_path/"stage";d=tmp_path/"dest";s.mkdir();d.mkdir()
    with pytest.raises(FileExistsError):atomic_publish(s,d)
def test_no_random_uuid_in_reference(framework_root): assert framework_root.name.startswith("FRAMEWORK_") and len(framework_root.name)==42
