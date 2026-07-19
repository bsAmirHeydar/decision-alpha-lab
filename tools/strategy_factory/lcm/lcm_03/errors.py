class LCM03Error(RuntimeError):
    """Base failure for LCM-03."""
class ContractViolation(LCM03Error): pass
class IntegrityError(LCM03Error): pass
class AuthorityError(LCM03Error): pass
class ResolutionError(LCM03Error): pass
class CollisionError(ResolutionError): pass
class UnknownVersionError(ResolutionError): pass
