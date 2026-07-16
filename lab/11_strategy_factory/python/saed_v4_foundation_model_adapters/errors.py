class V414Error(Exception):
    pass
class ContractError(V414Error): pass
class IntegrityError(V414Error): pass
class AuthorityError(V414Error): pass
class ContaminationError(V414Error): pass
class BudgetError(V414Error): pass
class QuarantineError(V414Error): pass
