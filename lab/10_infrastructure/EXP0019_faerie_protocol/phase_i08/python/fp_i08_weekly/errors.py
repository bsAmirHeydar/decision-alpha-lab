class FPI08Error(ValueError):
    def __init__(self,code,message,details=None):
        self.code=code; self.details=details or {}; super().__init__(f"{code}: {message}")
