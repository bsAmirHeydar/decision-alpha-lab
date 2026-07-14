class FPI13Error(ValueError):
    def __init__(self,code:str,message:str):
        super().__init__(f"{code}: {message}")
        self.code=code
        self.message=message
