"""Context package protocol, base implementation and immutable package registry."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Any, Iterable
from .manifest import ContextPackageManifest
from .lifecycle import ContextObservation
from .feature import FeatureDescriptor, FeatureFrame
from .representation import RepresentationViewDescriptor
from .cluster import ClusterRule
from .errors import RegistryError

class ContextPackage(ABC):
    @property
    @abstractmethod
    def manifest(self)->ContextPackageManifest: ...
    @abstractmethod
    def feature_descriptors(self)->tuple[FeatureDescriptor,...]: ...
    @abstractmethod
    def view_descriptors(self)->tuple[RepresentationViewDescriptor,...]: ...
    @abstractmethod
    def cluster_rules(self)->tuple[ClusterRule,...]: ...
    @abstractmethod
    def observe(self,source_record:Mapping[str,Any])->tuple[ContextObservation,...]: ...
    @abstractmethod
    def build_feature_frame(self,observation:ContextObservation,source_record:Mapping[str,Any])->FeatureFrame: ...

class ContextPackageRegistry:
    def __init__(self)->None: self._packages: dict[tuple[str,str],ContextPackage]={}
    def register(self,package:ContextPackage)->None:
        key=(package.manifest.package_id,package.manifest.version)
        if key in self._packages: raise RegistryError("duplicate_context_package","exact context package version already registered",{"package_id":key[0],"version":key[1]})
        self._packages[key]=package
    def resolve(self,package_id:str,version:str)->ContextPackage:
        package=self._packages.get((package_id,version))
        if package is None: raise RegistryError("context_package_not_found","exact context package version is not registered",{"package_id":package_id,"version":version})
        return package
    def descriptors(self)->tuple[tuple[str,str,str],...]: return tuple((p.manifest.package_id,p.manifest.version,p.manifest.manifest_hash) for _,p in sorted(self._packages.items()))
