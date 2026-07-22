class RTHPMT5Error(RuntimeError):
    def __init__(self, reason_code: str, message: str, details: dict | None = None):
        super().__init__(message)
        self.reason_code, self.details = reason_code, details or {}
