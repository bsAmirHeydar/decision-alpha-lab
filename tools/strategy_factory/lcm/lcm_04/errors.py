class LCM04Error(RuntimeError):
    """Base LCM-04 error."""
class ContractViolation(LCM04Error):
    """Closed contract violation."""
class IntegrityError(LCM04Error):
    """Artifact or upstream integrity failure."""
class AuthorityError(LCM04Error):
    """Authority permit failure."""
