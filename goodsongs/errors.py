"""Module to define specific errors."""


class NotFoundError(ValueError):
    """Raised when some application object could not be found."""


class InvalidRecordError(ValueError):
    """Raised when some application object did not passed validation."""
