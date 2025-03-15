from backend.application.exceptions.base import ApplicationError


class InvalidAmountError(ApplicationError):
    def __init__(self):
        super().__init__('Invalid amount for calculate exchange order')


class InvalidOrderStatusForConfirmationError(ApplicationError):
    def __init__(self):
        super().__init__('Invalid order status')
