class LCM08CError(RuntimeError):
    """Base error for LCM-08C."""

class UpstreamBindingError(LCM08CError):
    pass

class VerificationError(LCM08CError):
    pass

class AuthorityError(LCM08CError):
    pass
