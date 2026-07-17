class ACL01Error(Exception):
    """Base deterministic ACL-01 failure."""

class ContractError(ACL01Error): pass
class IdentityError(ACL01Error): pass
class RegistryError(ACL01Error): pass
class LocatorError(ACL01Error): pass
class CompatibilityError(ACL01Error): pass
class MigrationError(ACL01Error): pass
class IntegrityError(ACL01Error): pass
