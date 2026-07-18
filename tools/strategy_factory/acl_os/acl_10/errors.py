class ACL10Error(Exception): pass
class ContractError(ACL10Error): pass
class IntegrityError(ACL10Error): pass
class AuthorityError(ACL10Error): pass
class PolicyError(ACL10Error): pass
class TransitionError(ACL10Error): pass
class PublicationError(ACL10Error): pass
