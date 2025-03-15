from backend.application.exceptions.base import ApplicationError


class IncorrectUserIdError(ApplicationError):
    def __init__(self):
        super().__init__('Incorrect user_id')
