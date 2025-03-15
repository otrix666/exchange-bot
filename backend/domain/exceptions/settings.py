from backend.domain.exceptions.base import DomainError


class SettingsReadError(DomainError):
    def __init__(self):
        super().__init__('Settings read error')
