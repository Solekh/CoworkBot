from aiogram.fsm.state import StatesGroup, State


class ButtonsState(StatesGroup):
    lang = State()
    employee_menu = State()
    customer_menu = State()


class RegisterEmployeeState(StatesGroup):
    contact = State()
    description = State()
    category = State()
    job = State()

class RegisterCustomerState(StatesGroup):
    contact = State()
    first_name = State()
    last_name    = State()
    category = State()
    description = State()

class OrderState(StatesGroup):
    category = State()
    name = State()
    description = State()
    file = State()
    price = State()
    confirmed = State()


