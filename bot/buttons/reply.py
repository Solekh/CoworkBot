from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def main_menu():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text=_("🧑🏻‍💻 I am a freelancer")),
        KeyboardButton(text=_("👤 I am a customer")),
        KeyboardButton(text=_("💼 Vacancies/Vacancy placement")),
        KeyboardButton(text=_("Language 🇬🇧🇺🇿🇷🇺"))
    ])
    rkb.adjust(2, 1, 1)
    return rkb.as_markup(resize_keyboard=True)


def lang_buttons():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="English 🇬🇧"),
        KeyboardButton(text="O'zbek 🇺🇿"),
        KeyboardButton(text="Русский 🇷🇺"),
        KeyboardButton(text=_("⬅️ back"))
    ])
    rkb.adjust(3, 1)
    return rkb.as_markup(resize_keyboard=True)


def contact_button():
    contact_btn = KeyboardButton(text=_("☎️ Phone Number"), request_contact=True)
    return ReplyKeyboardMarkup(keyboard=[[contact_btn]], resize_keyboard=True)


def employee_menu():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text=_("My order")),
        KeyboardButton(text=_("Get Order")),
        KeyboardButton(text=_("Search Order")),
        KeyboardButton(text=_("My suggestion")),
        KeyboardButton(text=_("Balance")),
        KeyboardButton(text=_("Settings")),
        KeyboardButton(text=_("⬅️ back"))
    ])
    rkb.adjust(2, 2, 2, 1)
    return rkb.as_markup(resize_keyboard=True)


def order_btn():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text=_("📝My orders")),
        KeyboardButton(text=_("📤Order")),
        KeyboardButton(text=_("✅Freelancer suggestions")),
        KeyboardButton(text=_("💰Balance")),
        KeyboardButton(text=_("⚙️Settings")),
        KeyboardButton(text=_("⬅️ back")),
    ])
    rkb.adjust(2, 1, 2, 1)
    return rkb.as_markup(resize_keyboard=True)


def order_back(mandatory=True, back=True):
    rkb = ReplyKeyboardBuilder()
    if not mandatory:
        rkb.add(KeyboardButton(text=_("Next")))
    if back:
        rkb.add(KeyboardButton(text=_("⬅️ back")))

    rkb.add(KeyboardButton(text=_("🏠 Main Menu")))
    if not mandatory:
        if back:
            rkb.adjust(1, 2)

    return rkb.as_markup(resize_keyboard=True)


def confirmation_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text=_("✅ Confirm")),
        KeyboardButton(text=_("❌ Cancel")),
    ])
    rkb.adjust(1, 1)
    return rkb.as_markup(resize_keyboard=True)
