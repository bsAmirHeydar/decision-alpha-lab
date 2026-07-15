class OutcomeCubeError(Exception):
    pass  # Base fail-closed error for SAED V4-08.
class ContractError(OutcomeCubeError): pass
class AuthorityError(OutcomeCubeError): pass
class KnownTimeError(OutcomeCubeError): pass
class PathError(OutcomeCubeError): pass
class BudgetError(OutcomeCubeError): pass
class IntegrityError(OutcomeCubeError): pass
class QuarantineError(OutcomeCubeError): pass
