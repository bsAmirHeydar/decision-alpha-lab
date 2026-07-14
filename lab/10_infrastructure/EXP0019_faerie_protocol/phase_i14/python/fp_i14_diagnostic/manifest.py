from .contracts import ProductManifest
from .enums import ProductKind

def build_manifest(product,config_hash,source_revision_id="REV-I14-1",host_tf=5,product_version="1.0.0"):
    modules=tuple((f"FP-I{i:02d}","1.0.0") for i in range(3,14))
    return ProductManifest(ProductKind(product) if isinstance(product,str) else product,product_version,"FP-CONTEXT-001","FP-EPOCH-1","PAIR-ES-NQ",config_hash,source_revision_id,host_tf,modules)
