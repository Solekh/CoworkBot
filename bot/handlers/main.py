from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import html, Router, F
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.reply import main_menu, lang_buttons
from bot.dispatcher import dp
from bot.enums import LangEnum
from bot.state import ButtonsState
from db.models import User

main_router = Router()
@main_router.message(ButtonsState.customer_menu , F.text == __("⬅️ back"))
@main_router.message(ButtonsState.employee_menu , F.text == __("⬅️ back"))
@main_router.message(ButtonsState.lang , F.text == __("⬅️ back"))
@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_obj = User(id = message.from_user.id ,
                    first_name = message.from_user.first_name,
                    last_name = message.from_user.last_name)
    user = await user_obj.read()
    if not user:
        await user_obj.save(default=True)
    text = _("Hello, {fullname}!").format_map({"fullname": message.from_user.full_name})
    if message.text == __("⬅️ back"):
        text = _("Main menu")
    await message.answer(text, reply_markup=main_menu())

@main_router.message(F.text == __('Language 🇬🇧🇺🇿🇷🇺'))
async def lang_handler(message : Message , state : FSMContext):
    await state.set_state(ButtonsState.lang)
    await message.answer(_('Choose language'), reply_markup=lang_buttons())

@main_router.message(F.text.in_({"Русский 🇷🇺" , "O'zbek 🇺🇿" , "English 🇬🇧"}),ButtonsState.lang)
async def lang_choose_handler(message: Message , state : FSMContext , i18n):
    lang = LangEnum(message.text).name
    i18n.current_locale = lang
    await state.clear()
    await User(id = message.from_user.id).update(language = lang)
    await state.update_data({"locale" : lang})
    await message.answer(_("Language is selected !"), reply_markup=main_menu())








