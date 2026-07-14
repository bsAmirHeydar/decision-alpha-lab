class FPI10Error(ValueError):
    def __init__(self, reason_code: str, message: str):
        super().__init__(message)
        self.reason_code = reason_code
        self.message = message

class FPI10InitializationError(FPI10Error):
    pass

class FPI10CheckpointError(FPI10Error):
    pass
