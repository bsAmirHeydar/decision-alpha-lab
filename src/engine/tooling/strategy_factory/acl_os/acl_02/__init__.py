"""ACL-02 Context Standard and Intake reference implementation.

This package standardizes authored Context intake. It does not compile a
Context detector, train a model, select a setup, submit an order, or authorize
capital. Those authorities remain outside ACL-02.
"""
from .service import ACL02ContextIntakeService
from .types import IntakeDecision, ReadinessState
__all__=["ACL02ContextIntakeService","IntakeDecision","ReadinessState"]
__version__="1.0.0"
