class ACL15Error(RuntimeError): pass
class IntegrityError(ACL15Error): pass
class AuthorityError(ACL15Error): pass
class PolicyError(ACL15Error): pass
class ClosureError(ACL15Error): pass
