class ACL14Error(Exception): pass
class ContractError(ACL14Error): pass
class IntegrityError(ACL14Error): pass
class AuthorityError(ACL14Error): pass
class ReadinessError(ACL14Error): pass
class PublicationError(ACL14Error): pass
