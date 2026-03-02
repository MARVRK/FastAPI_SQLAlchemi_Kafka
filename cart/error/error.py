class CartError(Exception):
    def __init__(self, message, original_exception = None):
        self.message = message
        self.original_exception = original_exception
    def __str__(self):
        if self.original_exception:
            return f"(DB_CART_ERROR: {self.message}) caused by {repr(self.original_exception)}"
        return f"(DB_CART_ERROR: {self.message})"