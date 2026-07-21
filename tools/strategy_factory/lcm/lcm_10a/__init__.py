"""LCM-10A treatment and execution capability inventory.

This package is an authority-negative static evidence builder. It inventories
legacy Treatment atoms, broker-capable operations, reachability, ownership,
risk assumptions and unresolved evidence without importing or executing legacy
MQL5/Python strategy code.
"""
from .service import LCM10ATreatmentExecutionInventoryService
__all__ = ["LCM10ATreatmentExecutionInventoryService"]
