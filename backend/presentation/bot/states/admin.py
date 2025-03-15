from aiogram.fsm.state import State, StatesGroup


class UpdateSettings(StatesGroup):
    usdt_requisites = State()
    sell_usdt_rate = State()
    buy_usdt_rate = State()
    tg_chat_id = State()


class CreateMailing(StatesGroup):
    text = State()
    media = State()
    caption = State()
    button = State()
    confirm = State()


class CancelBuyOrder(StatesGroup):
    note = State()


class CancelSellOrder(StatesGroup):
    note = State()


class AddContact(StatesGroup):
    contact = State()


class SearchUser(StatesGroup):
    user_id = State()
    username = State()


class CreateTrxWithdraw(StatesGroup):
    amount = State()
    address = State()
    confirm = State()


class CreateUsdtWithdraw(StatesGroup):
    amount = State()
    address = State()
    confirm = State()


class AddCard(StatesGroup):
    card = State()
