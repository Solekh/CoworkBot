from enum import Enum
from aiogram.utils.i18n import gettext as _

class RoleEnum(Enum):
    admin = "Admin"
    user = "User"
    employee = "Employee"
    customer = "Customer"

class LangEnum(Enum):
    en = "English 🇬🇧"
    uz = "O'zbek 🇺🇿"
    ru = "Русский 🇷🇺"
