from pathlib import Path
import pytest
from conftest import ROOT
from saed_v4_execution_twin.models import ExecutionTwinProfile
import json

@pytest.mark.parametrize('path',sorted((ROOT/'lab/11_strategy_factory/examples/saed_v4_09/negative').glob('*.json')),ids=lambda p:p.name)
def test_every_negative_profile_fixture_fails(path:Path):
    with pytest.raises(Exception):ExecutionTwinProfile.from_mapping(json.loads(path.read_text()))
