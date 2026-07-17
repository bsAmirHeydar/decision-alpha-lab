"""ACL-01 repository identity, registries, locator, compatibility and lineage.

ACL-01 is a reference control-plane increment. It owns no trading, model
selection, live runtime or capital activation authority.
"""
from .service import ACL01RepositoryControlPlane
from .types import ArtifactDescriptor, ArtifactIdentity, LocatorResult, RegistryMutationPermit

__all__ = [
    "ACL01RepositoryControlPlane",
    "ArtifactDescriptor",
    "ArtifactIdentity",
    "LocatorResult",
    "RegistryMutationPermit",
]
__version__ = "1.0.0"
