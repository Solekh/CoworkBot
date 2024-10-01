from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from setuptools.errors import RemovedCommandError

from bot.buttons.inline import make_inline_button
from bot.buttons.reply import order_back, confirmation_button, order_btn
from bot.state import OrderState
from bot.utils import order_make_text
from db.models import Category, Project, Order

order_router = Router()


@order_router.message(OrderState.name, F.text == __("⬅️ back"))
@order_router.message(F.text == __("📤Order"))
async def order_button(msg: Message, state: FSMContext):
    await state.set_state(OrderState.category)
    categories = await Category().objects
    await msg.answer(_("Choose category !"), reply_markup=make_inline_button(categories, category=True, done=False))


@order_router.callback_query(OrderState.category)
async def order_button(call: CallbackQuery, state: FSMContext):
    text = _("Give the order a short name !")
    category = await Category(id=call.data).read()
    await state.update_data(
        {"category_id": int(call.data), "owner_id": call.from_user.id, "category_name": category.name})
    await state.set_state(OrderState.name)
    await call.message.delete()
    await call.message.answer(text, reply_markup=order_back())


@order_router.message(OrderState.name)
async def order_name_handler(msg: Message, state: FSMContext):
    text = _("Give the order a description !")
    await state.update_data({"name": msg.text})
    await state.set_state(OrderState.description)
    await msg.answer(text, reply_markup=order_back(back=False))


@order_router.message(OrderState.description)
async def order_description_handler(msg: Message, state: FSMContext):
    text = _("If there is a Technical Task related to the order, send it")
    await state.update_data({"description": msg.text})
    await state.set_state(OrderState.file)
    await msg.answer(text, reply_markup=order_back(back=False, mandatory=False))


@order_router.message(OrderState.file, F.document)
@order_router.message(OrderState.file, F.text == "Next")
async def document_file(msg: Message, state: FSMContext):
    text = _("Enter price ! , MIN : 50 000\nMAX : ♾")
    if msg.document:
        await state.update_data({"document": msg.document.file_id})
    await state.set_state(OrderState.price)
    await msg.answer(text, reply_markup=order_back(back=False))


@order_router.message(OrderState.price)
async def document_file(msg: Message, state: FSMContext):
    if msg.text >= "50000":
        await state.update_data({"price": msg.text})
        data = await state.get_data()
        language = data.get("locale")
        document = data.get("document")
        del data['locale']
        project_id = await Project(**data).save()
        order_id = await Order(project_id=project_id, ).save()
        data.update({"order_id": order_id})
        text = order_make_text(data)
        if document:
            success_document = await msg.answer_document(document=document, caption=text,
                                                         reply_markup=confirmation_button())
            await state.set_state(OrderState.confirmed)
            await state.update_data({"message_id": success_document.message_id})
            await state.update_data({"document": success_document.chat.id})
            await state.update_data({"order_id": order_id})
            await state.update_data({"project_id": project_id})
        else:
            success_txt = await msg.answer(text=text, reply_markup=confirmation_button())
            await state.update_data({"message_id": success_txt.message_id})
            await state.update_data({"text": success_txt.text})
            await state.update_data({"document": success_txt.chat.id})
            await state.set_state(OrderState.confirmed)
            await state.update_data({"order_id": order_id})
            await state.update_data({"project_id": project_id})
    else:
        await msg.answer(text=_("Price must be more than 50000"))
        await state.set_state(OrderState.price)


@order_router.message(F.text == __("✅ Confirm"))
@order_router.message(F.text == __("❌ Cancel"))
async def confirmation(message: Message, state: OrderState.confirmed):
    data = await state.get_data()
    if message.text == _("✅ Confirm"):
        from_chat_id = data["document"]
        msg_id = data["message_id"]
        await message.answer(text=_("Order has been confirmed!"), reply_markup=order_btn())
        await message.bot.forward_message(882090673, from_chat_id=from_chat_id, message_id=msg_id)
    else:
        order_id_ = data["order_id"]
        project_id = data["project_id"]
        msg_id = data["message_id"]
        await message.answer(text=_(F"Order has been canceled!\nOrder ID: {order_id_}, Project ID: {project_id}"),
                             reply_markup=order_btn())
        await message.bot.delete_message(message_id=int(msg_id), chat_id=message.chat.id)
        await Order(id=order_id_).delete()
        await Project(id=project_id).delete()
