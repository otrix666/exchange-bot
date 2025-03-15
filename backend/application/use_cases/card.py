from collections.abc import Sequence
from random import choice
from typing import Protocol
from uuid import UUID

from backend.application import exceptions, interfaces
from backend.config import Config
from backend.domain.entities.card import Card
from backend.domain.vo.requisites import CardRequisites


class GetCardsInteractor:
    def __init__(
        self,
        reader: interfaces.CardReader,
    ):
        self._reader = reader

    async def __call__(self, user_id: int) -> Sequence[Card]:
        cards = await self._reader.get_all_by_user_id(user_id=user_id)
        if not cards:
            raise exceptions.NoCardsError
        return cards


class GetCardInteractor:
    def __init__(
        self,
        reader: interfaces.CardReader,
        config: Config,
        uuid_generator: interfaces.UUIDGenerator,
    ):
        self._reader = reader
        self._config = config
        self._uuid_generator = uuid_generator

    async def __call__(self) -> Card:
        operators = self._config.bot.operators
        if not operators:
            raise ValueError('Список операторов пуст.')

        default_operator = operators[0]
        chosen_operator = (
            operators[1] if len(operators) > 1 and int(self._uuid_generator().hex, 16) % 2 == 0 else default_operator
        )

        cards = await self._reader.get_all_by_user_id(user_id=chosen_operator)

        if not cards and chosen_operator != default_operator:
            cards = await self._reader.get_all_by_user_id(user_id=default_operator)

        if not cards:
            raise exceptions.NoCardsError

        card = choice(cards)

        return card


class SaveCardInteractor:
    def __init__(
        self,
        saver: interfaces.CardSaver,
        uuid_generator: interfaces.UUIDGenerator,
    ):
        self._saver = saver
        self._uuid_generator = uuid_generator

    async def __call__(self, card_number: str, user_id: int) -> None:
        card = Card(
            id=self._uuid_generator(),
            number=CardRequisites(card_number=card_number),
            user_id=user_id,
            is_deleted=False,
        )
        await self._saver.save(card=card)


class DeleteCardManager(interfaces.CardReader, interfaces.CardDeleter, Protocol): ...


class DeleteCardInteractor:
    def __init__(
        self,
        delete_manager: DeleteCardManager,
    ):
        self._delete_manager = delete_manager

    async def __call__(self, card_id: UUID, user_id: int) -> Sequence[Card]:
        card = await self._delete_manager.get_by_id(card_id=card_id)
        card.is_deleted = True
        await self._delete_manager.delete_by_id(card=card)
        cards = await self._delete_manager.get_all_by_user_id(user_id=user_id)
        if not cards:
            raise exceptions.NoCardsError
        return cards
