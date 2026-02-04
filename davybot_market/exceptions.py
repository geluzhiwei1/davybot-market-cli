"""Exceptions for DavyBot Market SDK."""


class DavybotMarketError(Exception):
    """Base exception for DavyBot Market SDK."""

    pass


class AuthenticationError(DavybotMarketError):
    """Raised when authentication fails."""

    pass


class NotFoundError(DavybotMarketError):
    """Raised when a resource is not found."""

    pass


class ValidationError(DavybotMarketError):
    """Raised when request validation fails."""

    pass


class APIError(DavybotMarketError):
    """Raised when the API returns an error."""

    pass


class ConnectionError(DavybotMarketError):
    """Raised when connection to the API fails."""

    pass


class DownloadError(DavybotMarketError):
    """Raised when a download fails."""

    pass
