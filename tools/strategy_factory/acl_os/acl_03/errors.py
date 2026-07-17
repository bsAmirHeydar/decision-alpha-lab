class ACL03Error(Exception): """Base ACL-03 failure."""
class PrerequisiteError(ACL03Error): pass
class CompilationError(ACL03Error): pass
class IntegrityError(ACL03Error): pass
class SecurityBoundaryError(ACL03Error): pass
class ReplayError(ACL03Error): pass
