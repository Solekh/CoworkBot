from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

from bot.buttons.inline import make_inline_button
from bot.buttons.reply import contact_button, main_menu, employee_menu
from bot.enums import RoleEnum
from bot.state import RegisterEmployeeState, ButtonsState
from db.models import Category, Job, User, UserJob

employee_router = Router()


@employee_router.message(F.text == __('🧑🏻‍💻 I am a freelancer'))
async def freelancer_button_handler(message: Message, state: FSMContext):
    user = await User(id=message.from_user.id).read()
    if user and RoleEnum.employee.name in user.role:
        await state.set_state(ButtonsState.employee_menu)
        await message.answer(_("Employee Menu"), reply_markup=employee_menu())
    else:
        await state.set_state(RegisterEmployeeState.contact)
        await message.answer(_("Click the Send Contact button"), reply_markup=contact_button())


@employee_router.message(F.contact, RegisterEmployeeState.contact)
async def contact_handler(message: Message, state: FSMContext):
    await state.update_data({"phone_number": message.contact.phone_number})
    await state.set_state(RegisterEmployeeState.description)
    await message.answer(_("Briefly about yourself ✍🏻"), reply_markup=ReplyKeyboardRemove())


@employee_router.message(RegisterEmployeeState.description)
async def contact_handler(message: Message, state: FSMContext):
    await state.update_data({"description": message.text , "jobs" : []})
    await state.set_state(RegisterEmployeeState.category)
    categories: list[Category] = await Category().objects
    await message.answer(_("Choose your category !"), reply_markup=make_inline_button(categories, category=True))




@employee_router.callback_query(RegisterEmployeeState.job, F.data == "back")
async def contact_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegisterEmployeeState.category)
    categories: list[Category] = await Category().objects
    await callback.message.edit_text(_("Choose your category !"), reply_markup=make_inline_button(categories, category=True))

@employee_router.callback_query(RegisterEmployeeState.category,F.data == "done")
@employee_router.callback_query(RegisterEmployeeState.job,F.data == "done")
async def contact_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = await User(id=callback.from_user.id).read()
    if len(user.role) == 1 and RoleEnum.user.name in user.role:
        user.role[0] = RoleEnum.employee.name
    else:
        user.role.append(RoleEnum.employee.name)
    await User(id=callback.from_user.id).update(phone_number=data.get("phone_number").removeprefix("+"),
                                                description=data.get("description"), role=user.role)
    for job_id in data.get("jobs"):
        await UserJob(user_id=callback.from_user.id, job_id=job_id).save()
    await state.clear()
    await callback.message.delete()
    await state.set_state(ButtonsState.employee_menu)
    await state.update_data({"locale": data.get("locale")})
    await callback.message.answer(_("Success"), reply_markup=employee_menu())

@employee_router.callback_query(RegisterEmployeeState.category)
async def contact_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegisterEmployeeState.job)
    await state.update_data({"category_id": callback.data})
    data = await state.get_data()
    jobs = await Job(category_id=callback.data).filter_by_category()
    await callback.message.edit_text(_("Choose your job !"), reply_markup=make_inline_button(jobs , jobs = data.get("jobs")))


@employee_router.callback_query(RegisterEmployeeState.job)
async def contact_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    jobs : list = data.get("jobs")
    if (c:=int(callback.data)) in jobs:
        jobs.remove(c)
    else:
        jobs.append(c)
    await state.update_data({'jobs': jobs})
    await state.set_state(RegisterEmployeeState.job)
    jobs_list = await Job(category_id=data.get("category_id")).filter_by_category()
    await callback.message.edit_text(_("Choose your job !"), reply_markup=make_inline_button(jobs_list , jobs))




