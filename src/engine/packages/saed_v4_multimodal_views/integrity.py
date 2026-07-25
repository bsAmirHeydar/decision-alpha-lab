from .models import ViewIntegrityReceipt
from .canonical import merkle_root
from .errors import IntegrityError
def build_integrity_receipt(package):
    leaves=sorted([package.package_hash,package.lineage_root]+[v.view_hash for v in package.views]+[v.specification_hash for v in package.views])
    return ViewIntegrityReceipt(package.package_id,package.package_hash,tuple(sorted(v.view_hash for v in package.views)),tuple(sorted(v.specification_hash for v in package.views)),package.lineage_root,merkle_root(leaves),'pass')
def verify_integrity(package,receipt):
    current=build_integrity_receipt(package)
    if current.component_root!=receipt.component_root or current.package_hash!=receipt.package_hash:raise IntegrityError('view package integrity mismatch')
    return True
