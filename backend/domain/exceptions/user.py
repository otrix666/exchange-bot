from backend.domain.exceptions.base import DomainError


class UserNotFoundByIdError(DomainError):
    def __init__(self, user_id: int):
        super().__init__(f'User with id {user_id} not found')


class UserNotFoundByUsernameError(DomainError):
    def __init__(self, username: str):
        super().__init__(f'User with username {username} not found')


class UserPermissionError(DomainError):
    def __init__(self):
        super().__init__('User does not have permission')
