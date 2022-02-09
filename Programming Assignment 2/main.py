
import filters
import aiogram
from aiogram import types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import pathlib
import time
import os

bot = aiogram.Bot('1707342756:AAEa718cRjYcfa6RgiepiVrd1j-Q8sv1V0s')
dp = aiogram.Dispatcher(bot)
message_storage = []

@dp.message_handler(commands=["start"]) #decorator
async def cmd_start(message: types.Message):
    await message.answer('please send a pic')
    await bot.send_sticker(message.chat.id,
                           sticker='CAACAgIAAxkBAAECBCBgS30AAcKfN9L5niYlJ9mKXG5RccMAAkcAAyIVbQxuUoS0eFRQnR4E')


@dp.message_handler()
async def continue_asking(message: types.Message):
    await message.answer('please send a pic')

@dp.message_handler(content_types=["photo"])
async def adjust_pics(message: types.Message):
    message_storage.append(message)
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    blur = InlineKeyboardButton(text='Blur', callback_data='1')
    shades = InlineKeyboardButton(text='Shades', callback_data='2')
    bnw = InlineKeyboardButton(text='Black and White', callback_data='3')
    tricolor = InlineKeyboardButton(text='Tricolor', callback_data='4')
    bottom_right = InlineKeyboardButton(text='Bottom Right', callback_data='5')
    inline_keyboard.add(blur, shades, bnw, tricolor, bottom_right)
    await message.answer('Choose wisely', reply_markup=inline_keyboard)

@dp.callback_query_handler()
async def callback(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == "1" and len(message_storage) != 0:
        await call.message.answer('1 wait a bit...')
        await photo_processor(message_storage.pop(0), "1")
    elif call.data == "2" and len(message_storage) != 0:
        await call.message.answer('2 wait a bitу...')
        await photo_processor(message_storage.pop(0), "2")
    elif call.data == "3" and len(message_storage) != 0:
        await call.message.answer('3 wait a bit...')
        await photo_processor(message_storage.pop(0), "3")
    elif call.data == "4" and len(message_storage) != 0:
        await call.message.answer('4 wait a bit...')
        await photo_processor(message_storage.pop(0), "4")
    elif call.data == "5" and len(message_storage) != 0:
        await call.message.answer('5 wait a bit...')
        await photo_processor(message_storage.pop(0), "5")

async def photo_processor(message, filter_number):
    print(pathlib.Path().absolute())
    name_file = "img_" + str(time.strftime("%Y%m%d-%H%M%S")) + ".jpg"
    try:
        await message.photo[-1].download(name_file)
        img = filters.load_img(name_file)
        new_img = filters.filters_dictionary[filter_number](img)
        filters.save_img(new_img, name_file)
        await bot.send_message(message.from_user.id, filters.filters_dictionary_names[filter_number])
        await bot.send_photo(message.from_user.id, photo = open(name_file, "rb"))
        os.remove(name_file)
    except Exception as inst:
        print(inst)
        await bot.send_message(message.from_user.id, "whoopsie")

executor.start_polling(dp, skip_updates=True)

# print(pathlib.Path().absolute())
# print(str(time.strftime("%Y%m%d-%H%M%S")))
# try:
#     print(5 / 0)
#     print('problem2')
# except Exception as inst:
#     print(inst)
# print('problem3')

