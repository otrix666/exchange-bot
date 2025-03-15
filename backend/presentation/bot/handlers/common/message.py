from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, Message
from dishka import FromDishka

from backend.application import interfaces
from backend.config import Config
from backend.domain.templates.user_texts import main_menu_text

router = Router()


@router.message(CommandStart())
async def start_message(
    message: Message,
    config: FromDishka[Config],
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
) -> None:
    await message.answer_photo(
        photo=(
            FSInputFile(
                path=config.banner.file_path,
                filename='menu.jpg',
            )
        ),
        caption=main_menu_text(),
        reply_markup=kb_builder.get_main_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'close')
async def close_message(call: CallbackQuery):
    try:
        await call.answer()
        await call.message.delete()
    except:
        pass
