from __future__ import annotations

class ACL00Error(Exception):
    """Base exception for deterministic ACL-00 contract failures."""

class ContractError(ACL00Error):
    pass

class PolicyError(ACL00Error):
    pass

class IntegrityError(ACL00Error):
    pass

class ConcurrencyError(ACL00Error):
    pass
