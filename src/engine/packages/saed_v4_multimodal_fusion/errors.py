class V415Error(Exception): pass
class ContractError(V415Error): pass
class IntegrityError(V415Error): pass
class AuthorityError(V415Error): pass
class SupportError(V415Error): pass
class BudgetError(V415Error): pass
class QuarantineError(V415Error): pass
