from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def make_inline_button(data_list : list, jobs : list = [], category = False , done=True):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text =("✅" + i.name if i.id in jobs else i.name) , callback_data=f"{i.id}") for i in data_list
    ])
    ikb.add(
        *([InlineKeyboardButton(text=_("📌 Done") , callback_data="done")] if done else [] + ([] if category else [InlineKeyboardButton(text = _("🔙 back") , callback_data="back")]))
    )
    ikb.adjust(2 if category else 1, repeat=True)

    return ikb.as_markup()