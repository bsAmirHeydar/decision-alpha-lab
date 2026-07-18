class ACL08Error(Exception): pass
class ContractError(ACL08Error): pass
class IntegrityError(ACL08Error): pass
class AuthorityError(ACL08Error): pass
class PolicyError(ACL08Error): pass
class RedactionError(ACL08Error): pass
class PublicationError(ACL08Error): pass
