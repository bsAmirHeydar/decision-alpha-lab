class TreatmentDslError(Exception):
    """Base error for the SAED V4-06 finite Treatment DSL plane."""


class AuthorityError(TreatmentDslError):
    """Raised when a request exceeds the bounded V4-06 authority."""


class ContractError(TreatmentDslError):
    """Raised when a closed JSON contract is invalid."""


class RegistryError(TreatmentDslError):
    """Raised when the exact-version primitive registry is invalid."""


class ProgramError(TreatmentDslError):
    """Raised when a Treatment program is not a valid finite DSL program."""


class ParameterError(ProgramError):
    """Raised when a parameter violates type, unit, range, or closed-field rules."""


class CapabilityError(ProgramError):
    """Raised when a program requires an undeclared execution capability."""


class TemporalBoundaryError(TreatmentDslError):
    """Raised when known-time, event-time, or Evidence Role isolation fails."""


class BindingError(TreatmentDslError):
    """Raised when an immutable graph descriptor cannot be bound exactly."""


class IntegrityError(TreatmentDslError):
    """Raised when content identity, replay, or handoff verification fails."""
