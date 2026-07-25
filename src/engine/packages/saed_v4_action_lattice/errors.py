class ActionLatticeError(ValueError):
    """Base fail-closed error for SAED V4-07."""

class ContractError(ActionLatticeError):
    pass

class DomainError(ActionLatticeError):
    pass

class ConstraintError(ActionLatticeError):
    pass

class BudgetError(ActionLatticeError):
    pass

class IntegrityError(ActionLatticeError):
    pass
