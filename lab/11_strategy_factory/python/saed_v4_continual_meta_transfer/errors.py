class SAEDV425Error(Exception):
    """Base exception for the V4-25 research-only reference implementation."""


class ContractError(SAEDV425Error):
    """Raised when a closed contract is malformed or unsafe."""


class KnownTimeError(SAEDV425Error):
    """Raised when a record violates known-time discipline."""


class BudgetError(SAEDV425Error):
    """Raised when a frozen research budget would be exceeded."""


class UpstreamVerificationError(SAEDV425Error):
    """Raised when immutable V4-24 evidence cannot be verified."""


class SecurityBoundaryError(SAEDV425Error):
    """Raised on forbidden credentials, network endpoints, or authority claims."""
