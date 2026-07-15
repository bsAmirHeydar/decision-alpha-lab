class QualificationError(ValueError):
    """Fail-closed error raised when qualification evidence is invalid."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
