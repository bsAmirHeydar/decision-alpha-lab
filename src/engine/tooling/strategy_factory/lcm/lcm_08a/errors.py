class LCM08AError(RuntimeError):
    """Base LCM-08A failure."""

class UpstreamContractError(LCM08AError):
    """Upstream handoff is absent, malformed or not authoritative."""

class VerificationError(LCM08AError):
    """Package or installation verification failed."""

class PublicationError(LCM08AError):
    """Atomic publication failed."""
