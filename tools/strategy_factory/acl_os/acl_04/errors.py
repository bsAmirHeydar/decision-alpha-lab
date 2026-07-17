class ACL04Error(RuntimeError):
    """Base ACL-04 failure."""

class AuthorityError(ACL04Error):
    """Authority or handoff binding failed."""

class ContractError(ACL04Error):
    """A closed-schema or semantic contract failed."""

class ConstraintError(ACL04Error):
    """Candidate violates search or Treatment constraints."""

class SecurityBoundaryError(ACL04Error):
    """A path, capability, or forbidden operation crossed the boundary."""
