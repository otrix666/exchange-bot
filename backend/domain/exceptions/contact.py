from backend.domain.exceptions.base import DomainError


class ContactNotFoundError(DomainError):
    def __init__(self):
        super().__init__('Contact not found')
