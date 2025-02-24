class AuthenticationError(Exception):
    """Raised when authentication fails"""

    def __init__(self, message: str = 'Authentication failed') -> None:
        self.message = message
        super().__init__(self.message)


class AuthorizationError(Exception):
    """Raised when authorization fails"""

    def __init__(self, message: str = 'Authorization failed') -> None:
        self.message = message
        super().__init__(self.message)


class SecretKeyValidationError(Exception):
    """Raised when the provided secret key is invalid"""

    def __init__(self, message: str = 'Invalid secret key') -> None:
        self.message = message
        super().__init__(self.message)


class TokenExpiredError(Exception):
    """Raised when the JWT token has expired"""

    def __init__(self, message: str = 'Token has expired') -> None:
        self.message = message
        super().__init__(self.message)


class InvalidTokenError(Exception):
    """Raised when the JWT token is invalid"""

    def __init__(self, message: str = 'Invalid token') -> None:
        self.message = message
        super().__init__(self.message)
