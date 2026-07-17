"""ACL-04 Dual Setup Factory.

Compiles human-authored Setup DSL and bounded AI proposals into one canonical,
non-executable Setup Policy IR. The package is a research-definition control
plane only: it cannot submit orders, activate capital, mutate ACL-03 Context
semantics, or claim statistical edge.
"""
from .service import ACL04DualSetupFactoryService

__all__ = ["ACL04DualSetupFactoryService"]
