from backend.application.exceptions.base import ApplicationError


class IncorrectContactError(ApplicationError):
    def __init__(self):
        super().__init__('Incorrect contact information')
