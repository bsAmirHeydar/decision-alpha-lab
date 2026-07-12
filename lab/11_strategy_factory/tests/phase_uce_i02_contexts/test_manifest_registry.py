from __future__ import annotations
import pytest
from strategy_factory_contexts_v3 import *

def test_reference_manifest_identity_is_stable():
    a=SyntheticBreakContextPackage().manifest
    b=SyntheticBreakContextPackage().manifest
    assert a.manifest_hash==b.manifest_hash
    assert a.package_identity==b.package_identity
    assert a.package_id=="ucee.reference.synthetic_break"

def test_exact_version_registry():
    registry=ContextPackageRegistry(); a=SyntheticBreakContextPackage(); b=EXP0017ContextPackage()
    registry.register(a); registry.register(b)
    assert registry.resolve(a.manifest.package_id,a.manifest.version) is a
    assert len(registry.descriptors())==2
    with pytest.raises(RegistryError): registry.register(SyntheticBreakContextPackage())
    with pytest.raises(RegistryError): registry.resolve(a.manifest.package_id,"9.9.9")

def test_manifest_rejects_mutable_metadata():
    p=SyntheticBreakContextPackage().manifest
    with pytest.raises(ManifestError):
        ContextPackageManifest(p.package_id,p.version,p.owner_id,p.doctrine_id,p.doctrine_version,p.anatomy_adapter_id,p.anatomy_adapter_version,p.update_scope,p.runtime_modes,p.source_requirements,p.feature_packs,p.representation_views,p.cluster_rules,p.manual_policies,p.tasks,p.parent_package_id,p.description,{"created_at":"now"})

def test_source_requirement_validation():
    with pytest.raises(ManifestError): SourceRequirement("x",SourceRequirementKind.CLOSED_BARS,RequirementStrength.REQUIRED,(),60,1,0,"none","")
    with pytest.raises(ManifestError): SourceRequirement("x",SourceRequirementKind.CLOSED_BARS,RequirementStrength.REQUIRED,("EURUSD",),-1,1,0,"none","")
