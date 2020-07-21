class PretixException(Exception):
    """
    Base exception thrown when using Pretix
    """


class InvalidDataError(PretixException):
    """
    Thrown when request contains invalid data.
    Equivalent to status code 400
    """


class AuthenticationError(PretixException):
    """
    Thrown when request is unauthenticated
    Equivalent to status code 401
    """


class AuthorizationError(PretixException):
    """
    Thrown when request is unauthorized
    Equivalent to status code 403
    """


class ConflictError(PretixException):
    """
    Thrown when a second request for the generation of a ticket.
    Equivalent to status code 409
    """
