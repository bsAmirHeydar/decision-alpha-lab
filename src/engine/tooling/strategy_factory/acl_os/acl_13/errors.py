class ACL13Error(Exception): pass
class ContractError(ACL13Error): pass
class IntegrityError(ACL13Error): pass
class AuthorityError(ACL13Error): pass
class BudgetError(ACL13Error): pass
class AssessmentError(ACL13Error): pass
class PublicationError(ACL13Error): pass
