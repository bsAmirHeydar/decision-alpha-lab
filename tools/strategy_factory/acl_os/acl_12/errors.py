class ACL12Error(Exception): pass
class ContractError(ACL12Error): pass
class IntegrityError(ACL12Error): pass
class AuthorityError(ACL12Error): pass
class PolicyError(ACL12Error): pass
class SecurityError(ACL12Error): pass
class PublicationError(ACL12Error): pass
