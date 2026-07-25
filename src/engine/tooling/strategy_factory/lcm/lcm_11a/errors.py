class LCM11AError(RuntimeError):
    """Base error for deterministic LCM-11A validation failures."""

class ContractError(LCM11AError):
    pass

class InventoryError(LCM11AError):
    pass
