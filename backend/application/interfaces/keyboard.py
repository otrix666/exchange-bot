from abc import abstractmethod
from collections.abc import Sequence
from typing import Any, Protocol
from uuid import UUID

from backend.domain.entities.card import Card
from backend.domain.entities.contact import Contact


class Keyboard(Protocol):
    def as_markup(self) -> Any: ...


class AdminKeyboardBuilder(Protocol):
    @abstractmethod
    def get_admin_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_settings_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_wallet_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_wallet_manu_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_withdraw_confirmation_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_card_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_delete_card_menu(self, cards: Sequence[Card]) -> Keyboard: ...

    @abstractmethod
    def get_card_menu_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_settings_menu_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_admin_menu_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_users_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_mailing_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_users_menu_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_search_user_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_user_details_menu_kb(self, user_id: int, is_banned: bool) -> Keyboard: ...

    @abstractmethod
    def get_admin_contacts_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_remove_contact_kb(self, contacts: Sequence[Contact]) -> Keyboard: ...

    @abstractmethod
    def get_admin_contacts_menu_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_order_confirm_kb(
        self,
        order_id: UUID,
        order_type: str,
        is_banned: bool,
    ) -> Keyboard: ...

    @abstractmethod
    def get_return_sell_order_kb(self, order_id: int) -> Keyboard: ...

    @abstractmethod
    def get_return_buy_order_kb(self, order_id: int) -> Keyboard: ...

    @abstractmethod
    def get_close_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_custom_kb(self, text: str, url: str) -> Keyboard: ...

    @abstractmethod
    def get_operator_notifications_kb(self, chat_id: str, message_id: str) -> Keyboard: ...


class UserKeyboardBuilder(Protocol):
    @abstractmethod
    def get_main_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_main_menu_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_profile_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_exchange_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_exchange_menu_return_kb(self) -> Keyboard: ...

    def get_contact_menu_kb(self, contacts: Sequence[Contact]) -> Keyboard: ...
