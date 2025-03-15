from backend.application.exceptions.base import ApplicationError


class NoCardsError(ApplicationError):
    def __init__(self):
        super().__init__('No cards was found.')


class CardNotFoundByIdError(ApplicationError):
    def __init__(self):
        super().__init__('No card was found.')
