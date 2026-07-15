class ExecutionTwinError(ValueError):
    """Base fail-closed error for SAED V4-09."""

class ContractError(ExecutionTwinError):
    pass

class AuthorityError(ExecutionTwinError):
    pass

class IntegrityError(ExecutionTwinError):
    pass

class BudgetError(ExecutionTwinError):
    pass

class BrokerConstraintError(ExecutionTwinError):
    pass
