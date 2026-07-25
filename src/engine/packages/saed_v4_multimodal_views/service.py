from .registry import ViewSpecificationRegistry,ViewArtifactRegistry
from .builder import ViewBuilder
from .package import MultimodalPackageBuilder
from .replay import ViewReplayer
from .integrity import build_integrity_receipt
class MultimodalViewService:
    def __init__(self):
        self.specifications=ViewSpecificationRegistry();self.artifacts=ViewArtifactRegistry();self.builder=ViewBuilder();self.packages=MultimodalPackageBuilder();self.replayer=ViewReplayer(self.builder)
    def register_specification(self,spec):return self.specifications.register(spec)
    def build_view(self,spec,request):
        view=self.builder.build(spec,request);return self.artifacts.register(view)
    def build_package(self,views,package_version,required_view_names,optional_view_names=(),limitations=()):return self.packages.build(views,package_version,required_view_names,optional_view_names,limitations)
    def integrity_receipt(self,package):return build_integrity_receipt(package)
