from __future__ import annotations
import json
from pathlib import Path
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[4]
EXAMPLES = ROOT / "lab/11_strategy_factory/examples/saed_v4_00"
SCHEMAS = ROOT / "lab/11_strategy_factory/schemas/saed_v4_00"

@pytest.fixture
def constitution_doc():
    return yaml.safe_load((EXAMPLES / "research_constitution.yaml").read_text(encoding="utf-8"))

@pytest.fixture
def constitution_hash(constitution_doc):
    from saed_v4_constitution.canonical import content_hash
    return content_hash(constitution_doc)

@pytest.fixture
def kernel(constitution_hash):
    from saed_v4_constitution.policy import ConstitutionKernel
    return ConstitutionKernel(constitution_hash)

@pytest.fixture
def agent():
    from saed_v4_constitution.models import Actor
    from saed_v4_constitution.enums import ActorType
    return Actor("agent-1", ActorType.AGENT, "research-ai", ("hypothesis",))

@pytest.fixture
def researcher():
    from saed_v4_constitution.models import Actor
    from saed_v4_constitution.enums import ActorType
    return Actor("researcher-1", ActorType.HUMAN_RESEARCHER, "research", ("owner",))
