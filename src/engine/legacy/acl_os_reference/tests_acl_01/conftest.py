from __future__ import annotations
from datetime import datetime,timedelta,timezone
from pathlib import Path
import pytest
from src.engine.tooling.strategy_factory.acl_os.acl_01.canonical import digest_file
from src.engine.tooling.strategy_factory.acl_os.acl_01.identity import build_artifact_id
from src.engine.tooling.strategy_factory.acl_os.acl_01.policies import PolicyBundle
from src.engine.tooling.strategy_factory.acl_os.acl_01.registry import RepositoryRegistry
from src.engine.tooling.strategy_factory.acl_os.acl_01.types import ArtifactDescriptor,ArtifactIdentity,ArtifactMutability,RegistryMutationPermit
from src.engine.tooling.strategy_factory.acl_os.acl_00.catalogs import PolicyBundle as ACL00PolicyBundle

@pytest.fixture
def policies(): return PolicyBundle.load()

@pytest.fixture
def permit_factory():
    def make(action,tenant="alpha",subject="al://system/acl-os/repository-registry@1.0.0"):
        now=datetime.now(timezone.utc)
        return RegistryMutationPermit("DEC_TEST_001","ALLOW",tenant,subject,action,ACL00PolicyBundle.load().digest,now-timedelta(minutes=1),now+timedelta(hours=1),False,False)
    return make

@pytest.fixture
def registry(policies,permit_factory):
    r=RepositoryRegistry(policies)
    r.owners["OWNER_TEST"]={"tenant_id":"alpha","display_name":"Test Owner","roles":["SEMANTIC_OWNER","TECHNICAL_OWNER","SCHEMA_STEWARD","PLUGIN_OWNER","RUNTIME_OWNER","SECURITY_OWNER","POLICY_STEWARD"],"status":"ACTIVE","review_routes":["test"]}
    r.schemas["schema:test:1"]={"tenant_id":"alpha","version":"1.0.0","path":"registry/test.json","digest":"sha256:"+"1"*64,"status":"ACTIVE"}
    return r

@pytest.fixture
def artifact_file(tmp_path):
    p=tmp_path/"contexts/legacy/strategy_factory/authored/ctx-test/doctrine/context.md"; p.parent.mkdir(parents=True); p.write_text("context\n",encoding="utf-8"); return p

@pytest.fixture
def descriptor(artifact_file,tmp_path):
    version="1.0.0"; aid=build_artifact_id("alpha","research","context_doctrine","ctx-test",version)
    return ArtifactDescriptor(ArtifactIdentity(aid,"alpha","research","context_doctrine","ctx-test",version,digest_file(artifact_file)),"context_authored","contexts/legacy/strategy_factory/authored/ctx-test/doctrine/context.md","domain","OWNER_TEST","schema:test:1","CONFIDENTIAL",ArtifactMutability.AUTHORED,metadata={"interfaces":{"context.read":"1.0.0"},"schema_semver":"1.0.0","visibility":"PUBLIC"})
