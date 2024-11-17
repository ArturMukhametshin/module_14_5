from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import initiate_db, get_all_products, add_user, is_included

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')
button_4 = KeyboardButton(text='Регистрация')
kb.add(button_1)
kb.add(button_2)
kb.add(button_3)
kb.add(button_4)

ikb = InlineKeyboardMarkup()
i_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
i_button2 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
ikb.add(i_button)
ikb.add(i_button2)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ]
)

users = get_all_products()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('images/1.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: {users[0][0]}  |  Описание: {users[0][1]}  |  Цена: {users[0][2]}')
    with open('images/2.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: {users[1][0]}  |  Описание: {users[1][1]}  |  Цена: {users[1][2]}')
    with open('images/3.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: {users[2][0]}  |  Описание: {users[2][1]}  |  Цена: {users[2][2]}')
    with open('images/4.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: {users[3][0]}  |  Описание: {users[3][1]}  |  Цена: {users[3][2]}')
    await message.answer('Выберете продукт для покупки:', reply_markup=catalog_kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('(10 × вес в кг) + (6,25 × рост в см) '
                              '− (5 × возраст в годах) + 5')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью',
                         reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = int(9.99 * int(data['weight']) + 6.25 * int(data['growth'])
                 - 4.92 * int(data['age']) + 5)
    await message.answer(f'Ваша норма потребления каллорий'
                         f' в сутки: {result} Ккал.')
    await state.finish()

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(usnam=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(em=message.text)
    await message.answer('Введите свой возраст: ')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(ag=message.text)
    data = await state.get_data()
    add_user(data['usnam'], data['em'], data['ag'])
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, что бы начать'
                         ' пользоваться нашим ботом')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)