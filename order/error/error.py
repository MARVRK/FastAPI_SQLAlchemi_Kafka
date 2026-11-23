class ServiceUnavailable(Exception):
    code = "SERVICE_UNAVAILABLE"
    def __init__(self, service):
        self.service = service
        self.message = f"{self.service} service unavailable"
        super().__init__(self.message)

class CartUnavailable(ServiceUnavailable):
    def __init__(self):
        super().__init__(service="cart")


class ProductUnavailable(ServiceUnavailable):
    def __init__(self):
        super().__init__(service="product")
