from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

api = '🤔'
bot = Bot(token=api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup()
inform = KeyboardButton(text='Информация')
calculate = KeyboardButton(text='Рассчитать')
kb.add(inform)
kb.add(calculate)

ikc = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text = "Рассчитать норму каллорий", callback_data='calories')
button2 = InlineKeyboardButton(text= 'Формулы расчёта', callback_data= 'formulas')
ikc.add(button1)
ikc.add(button2)
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands='start')
async def start(message):
    print("Напечатан /start")
    await message.answer('Привет! Я бот помогающий твоему здороью.', reply_markup= ikc)

@dp.callback_query_handler(text='calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(text = 'Информация')
async def all_massages(message):
    print(f'Информация')
    await message.answer('🤔')

@dp.message_handler()
async def all_massages(message):
    print(f'Напечатан {message.text}')
    await message.answer('Введите команду /start, чтобы начать общение.')

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) - 5 x возраст (г) + 5')
    await call.answer()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth = message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    calories = 60 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
