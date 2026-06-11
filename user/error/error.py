class UserError(Exception):
    def __init__(self, message: str, original_exception=None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(message)

    def __str__(self):
        if self.original_exception:
            return f"(USER_ERROR: {self.message}) caused by {self.original_exception}"
        return f"(USER_ERROR: {self.message})"


class AuthError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
