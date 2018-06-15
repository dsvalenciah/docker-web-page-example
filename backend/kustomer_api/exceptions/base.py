class KustomerApiError(Exception):
    """Encapsulates our exceptions."""

class RequestError(KustomerApiError):
    """A definition is not well defined."""
