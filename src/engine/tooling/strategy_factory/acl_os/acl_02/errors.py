class ACL02Error(Exception): """Base deterministic ACL-02 failure."""
class ContractError(ACL02Error): pass
class PackageLoadError(ACL02Error): pass
class IntakeError(ACL02Error): pass
class SecurityClassificationError(ACL02Error): pass
class AuthorityBindingError(ACL02Error): pass
