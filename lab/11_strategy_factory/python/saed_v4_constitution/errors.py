"""Typed errors for the SAED V4 constitutional control plane."""

class ConstitutionError(Exception):
    """Base error for deterministic constitutional failures."""


class ContractError(ConstitutionError):
    """A closed contract is malformed or contains unknown fields."""


class AuthorityViolation(ConstitutionError):
    """A request attempts to exercise authority not granted by the constitution."""


class EvidenceRoleViolation(ConstitutionError):
    """A request violates protected evidence-role boundaries."""


class IndependenceViolation(ConstitutionError):
    """Required reviewer or proposer independence is absent."""


class IntegrityViolation(ConstitutionError):
    """A hash, ledger, signature, or lineage invariant is broken."""


class AmendmentViolation(ConstitutionError):
    """A constitutional amendment is invalid, retroactive, or self-approved."""


class WaiverViolation(ConstitutionError):
    """A waiver attempts to bypass a non-waivable rule or lacks expiry."""
