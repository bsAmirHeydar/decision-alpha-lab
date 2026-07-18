class ACL11Error(Exception): pass
class ContractError(ACL11Error): pass
class IntegrityError(ACL11Error): pass
class AuthorityError(ACL11Error): pass
class PolicyError(ACL11Error): pass
class CustodyError(ACL11Error): pass
class PublicationError(ACL11Error): pass
