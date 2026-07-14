class FPI11Error(ValueError):
    def __init__(self,code,message): self.code=code; super().__init__(f'{code}: {message}')
class FPI11ImmutableViolation(FPI11Error): pass
