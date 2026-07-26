from pathlib import Path
import pytest
from src.engine.tooling.strategy_factory.lcm.lcm_02.io import atomic_publish

def test_non_empty_destination_rejected(tmp_path):
 s=tmp_path/'s';d=tmp_path/'d';s.mkdir();d.mkdir();(d/'x').write_text('x')
 with pytest.raises(FileExistsError): atomic_publish(s,d)
