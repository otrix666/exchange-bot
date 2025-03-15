from aiogram.fsm.state import State, StatesGroup


class CreateBuyExchangeOrder(StatesGroup):
    requisites = State()
    amount = State()
    cheque = State()


class CreateSellExchangeOrder(StatesGroup):
    requisites = State()
    amount = State()
    cheque = State()
