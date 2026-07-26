"""Read-only ACL-04 bridge to LCM-10B reference Treatment bindings.
This bridge cannot evaluate legacy sources, activate adapters, or submit orders.
"""
from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_10b.factory_bridge import LCM10BFactoryReference
def load_lcm10b_reference(migration_root:Path)->LCM10BFactoryReference:return LCM10BFactoryReference(migration_root)
