class BaselineManualError(ValueError):
    """Base fail-closed error for SAED V4-10."""
class ContractError(BaselineManualError): pass
class AuthorityError(BaselineManualError): pass
class IntegrityError(BaselineManualError): pass
class LeakageError(BaselineManualError): pass
class CompilationError(BaselineManualError): pass
class EvaluationError(BaselineManualError): pass
