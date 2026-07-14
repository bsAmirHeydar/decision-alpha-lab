"""Domain errors for the sovereign data and artifact foundation."""
class DataFoundationError(Exception):
    """Base failure."""
class ContractError(DataFoundationError): pass
class TemporalIntegrityError(DataFoundationError): pass
class IntegrityViolation(DataFoundationError): pass
class ImmutableConflict(DataFoundationError): pass
class LineageCycleError(DataFoundationError): pass
class RoleViolation(DataFoundationError): pass
class QuarantineRequired(DataFoundationError): pass
class AccessDenied(DataFoundationError): pass
class ReplayError(DataFoundationError): pass
