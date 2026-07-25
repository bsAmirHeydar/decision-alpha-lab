class SAEDV424Error(Exception):
    """Base V4-24 error."""

class ContractError(SAEDV424Error): pass
class IntegrityError(SAEDV424Error): pass
class AuthorityError(SAEDV424Error): pass
class UpstreamError(SAEDV424Error): pass
class BudgetError(SAEDV424Error): pass
class DatasetError(SAEDV424Error): pass
class ConformalError(SAEDV424Error): pass
class OODError(SAEDV424Error): pass
class SelectiveControlError(SAEDV424Error): pass
class DriftError(SAEDV424Error): pass
class CertificateError(SAEDV424Error): pass
