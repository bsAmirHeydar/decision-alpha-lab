class LCM02Error(RuntimeError):
    """Base LCM-02 failure."""
class ContractViolation(LCM02Error): pass
class IntegrityError(LCM02Error): pass
class AuthorityError(LCM02Error): pass
