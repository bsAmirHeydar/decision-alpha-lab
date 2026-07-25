class MechanisticInterpretabilityError(Exception):
    """Base error for the V4-26 research boundary."""

class ContractError(MechanisticInterpretabilityError):
    pass

class KnownTimeError(MechanisticInterpretabilityError):
    pass

class UpstreamVerificationError(MechanisticInterpretabilityError):
    pass

class SecurityBoundaryError(MechanisticInterpretabilityError):
    pass

class BudgetError(MechanisticInterpretabilityError):
    pass

class AuthorityError(MechanisticInterpretabilityError):
    pass
