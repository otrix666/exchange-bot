from collections.abc import Sequence
from typing import Protocol

from backend.application import exceptions, interfaces
from backend.domain.entities.contact import Contact


class GetContactsInteractor:
    def __init__(
        self,
        reader: interfaces.ContactReader,
    ):
        self._reader = reader

    async def __call__(self) -> Sequence[Contact]:
        contacts = await self._reader.get_all()
        return contacts


class SaveContactInteractor:
    def __init__(
        self,
        saver: interfaces.ContactSaver,
    ):
        self._saver = saver

    async def __call__(self, contact: str) -> None:
        if '|' not in contact:
            raise exceptions.IncorrectContactError

        title, url = contact.split('|')

        if 'http' not in url:
            raise exceptions.IncorrectContactError

        contact = Contact(
            id=None,
            title=title,
            url=url,
        )

        await self._saver.save(contact=contact)


class DeleteContactManager(interfaces.ContactReader, interfaces.ContactDeleter, Protocol): ...


class DeleteContactInteractor:
    def __init__(
        self,
        delete_manager: DeleteContactManager,
    ):
        self._delete_manager = delete_manager

    async def __call__(self, contact_id: int) -> Sequence[Contact]:
        contact = await self._delete_manager.get_by_id(contact_id=contact_id)
        await self._delete_manager.delete_by_id(contact=contact)
        contacts = await self._delete_manager.get_all()

        return contacts
