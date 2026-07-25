class HypergraphError(Exception):
    """Base error for the SAED V4-05 semantic-temporal hypergraph plane."""


class AuthorityError(HypergraphError):
    """Raised when a request exceeds the phase authority boundary."""


class ContractError(HypergraphError):
    """Raised when a closed contract cannot be validated."""


class RegistryError(HypergraphError):
    """Raised when a semantic registry is invalid or cannot resolve a relation."""


class TemporalBoundaryError(HypergraphError):
    """Raised when bitemporal visibility or interval invariants are violated."""


class GraphBuildError(HypergraphError):
    """Raised when deterministic graph construction cannot complete safely."""


class GraphValidationError(HypergraphError):
    """Raised when a graph violates a structural or semantic invariant."""


class IntegrityError(HypergraphError):
    """Raised when replay or integrity verification fails."""


class QueryError(HypergraphError):
    """Raised when a bounded graph query is invalid or exceeds budget."""
