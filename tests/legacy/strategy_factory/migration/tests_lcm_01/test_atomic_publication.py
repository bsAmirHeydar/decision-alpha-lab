import pytest
from pathlib import Path
from tools.strategy_factory.lcm.lcm_01.service import RunConfig, run_survey

def test_non_empty_destination_rejected(repo_root,tmp_path):
    d=tmp_path/'out'; d.mkdir(); (d/'occupied').write_text('x')
    with pytest.raises(FileExistsError): run_survey(RunConfig(repo_root,d))
