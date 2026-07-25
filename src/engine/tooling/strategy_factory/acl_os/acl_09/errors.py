class ACL09Error(Exception): pass
class ContractError(ACL09Error): pass
class IntegrityError(ACL09Error): pass
class AuthorityError(ACL09Error): pass
class PolicyError(ACL09Error): pass
class PoisoningError(ACL09Error): pass
class PublicationError(ACL09Error): pass
