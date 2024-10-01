from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.reply import contact_button, order_btn, order_back
from bot.enums import RoleEnum
from bot.state import RegisterCustomerState, ButtonsState, OrderState
from db.models import User, Order

customer_router = Router()


@customer_router.message(OrderState.price, F.text == __("🏠 Main Menu"))
@customer_router.message(OrderState.file, F.text == __("🏠 Main Menu"))
@customer_router.message(OrderState.description, F.text == __("🏠 Main Menu"))
@customer_router.message(OrderState.name, F.text == __("🏠 Main Menu"))
@customer_router.message(RegisterCustomerState.first_name, F.text == __("🏠 Main Menu"))
@customer_router.message(RegisterCustomerState.first_name, F.text == __("⬅️ back"))
@customer_router.message(RegisterCustomerState.last_name, F.text == __("⬅️ back"))
@customer_router.message(RegisterCustomerState.last_name, F.text == __("🏠 Main Menu"))
@customer_router.message(F.text == __("👤 I am a customer"))
async def customer_click_button(msg: Message, state: FSMContext):
    user = await User(id=msg.from_user.id).read()
    if user and RoleEnum.customer.name in user.role:
        await state.set_state(ButtonsState.customer_menu)
        await msg.answer(_("Welcome cabinet !"), reply_markup=order_btn())
    else:
        text = _("Enter your first name !")
        await state.set_state(RegisterCustomerState.first_name)
        await msg.answer(text, reply_markup=order_back())


@customer_router.message(RegisterCustomerState.first_name)
async def first_name_button(msg: Message, state: FSMContext):
    text = _("Enter your last name !")
    await state.update_data({"first_name": msg.text})
    await state.set_state(RegisterCustomerState.last_name)
    await msg.answer(text)


@customer_router.message(RegisterCustomerState.last_name)
async def first_name_button(msg: Message, state: FSMContext):
    text = _("Click button contact !")
    await state.update_data({"last_name": msg.text})
    await state.set_state(RegisterCustomerState.contact)
    await msg.answer(text, reply_markup=contact_button())


@customer_router.message(RegisterCustomerState.contact)
async def first_name_button(msg: Message, state: FSMContext):
    text = _("Welcome cabinet !")
    data = await state.get_data()
    language = data.get("locale")
    await state.clear()
    await state.update_data({"locale": language})
    phone_number = msg.contact.phone_number.removeprefix("+")
    user = await User(id=msg.from_user.id).read()
    if len(user.role) == 1 and RoleEnum.user.name in user.role:
        user.role[0] = RoleEnum.customer.name
    else:
        user.role.append(RoleEnum.customer.name)
    del data['locale']
    await user.update(**data, phone_number=phone_number, language=language, role=user.role)
    await msg.answer(text, reply_markup=order_btn())


@customer_router.message(F.text == __("📝My orders"))
async def my_orders_handler(msg: Message, state: FSMContext):
    orders = await Order(employee_id=msg.from_user.id).read()
    texts = _("Your orders:")
    if orders:
        for order in orders:
            await msg.answer(text=f"#{order.id}, {order.project_id}")
    else:
        await msg.answer("You not a orders!")
