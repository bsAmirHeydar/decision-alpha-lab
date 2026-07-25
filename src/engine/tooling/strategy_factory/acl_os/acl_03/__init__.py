"""ACL-03 Context Compiler and Onboarding Factory.

The package compiles semantically approved ACL-02 Context packages into a
closed, deterministic, non-trading intermediate representation and onboarding
evidence. It does not generate executable trading code or grant research,
runtime, capital, or live-order authority.
"""
from .service import ACL03ContextCompilerService
__all__ = ["ACL03ContextCompilerService"]
