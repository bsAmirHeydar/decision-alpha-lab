class LCM00Error(RuntimeError):
    """Base LCM-00 error."""


class ContractViolation(LCM00Error):
    """Raised when a closed contract is violated."""


class IntegrityError(LCM00Error):
    """Raised when content or lineage integrity fails."""


class AuthorityError(LCM00Error):
    """Raised when authority or role-separation checks fail."""


class DestinationConflict(LCM00Error):
    """Raised when atomic output destination is not empty."""
