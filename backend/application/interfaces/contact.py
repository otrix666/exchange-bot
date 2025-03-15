from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from backend.domain.entities.contact import Contact


class ContactReader(Protocol):
    @abstractmethod
    async def get_by_id(self, contact_id: int) -> Contact: ...

    @abstractmethod
    async def get_all(self) -> Sequence[Contact]: ...


class ContactSaver(Protocol):
    @abstractmethod
    async def save(self, contact: Contact) -> None: ...


class ContactDeleter(Protocol):
    @abstractmethod
    async def delete_by_id(self, contact: Contact) -> None: ...
