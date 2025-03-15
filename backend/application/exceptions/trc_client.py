from backend.application.exceptions.base import ApplicationError


class NotEnoughTrxForTransferError(ApplicationError):
    def __init__(self):
        super().__init__('Not enough trx for transfer')


class NotEnoughTrxForCommissionError(ApplicationError):
    def __init__(self):
        super().__init__('Not enough trx for commission')


class NotEnoughUsdtForTransferError(ApplicationError):
    def __init__(self):
        super().__init__('Not enough usdt for transfer')


class IncorrectWithdrawAmountError(ApplicationError):
    def __init__(self):
        super().__init__('Incorrect withdraw amount')


class TransactionError(ApplicationError):
    def __init__(self):
        super().__init__('Transaction error')
