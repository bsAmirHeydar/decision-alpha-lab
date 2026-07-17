class SAEDV432Error(Exception):
    """Base error for the V4-32 reference implementation."""

class ContractError(SAEDV432Error): pass
class UpstreamError(SAEDV432Error): pass
class ConstitutionError(SAEDV432Error): pass
class AuthorityError(SAEDV432Error): pass
class IdentityError(SAEDV432Error): pass
class TaskError(SAEDV432Error): pass
class ProvenanceError(SAEDV432Error): pass
class ReviewError(SAEDV432Error): pass
class BudgetError(SAEDV432Error): pass
class IncidentError(SAEDV432Error): pass
