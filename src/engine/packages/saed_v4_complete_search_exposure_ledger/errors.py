class SAEDV427Error(Exception):
    """Base error for the V4-27 closed research ledger."""
class ContractError(SAEDV427Error): pass
class IntegrityError(SAEDV427Error): pass
class StateTransitionError(SAEDV427Error): pass
class BudgetExceededError(SAEDV427Error): pass
class AuthorityBoundaryError(SAEDV427Error): pass
