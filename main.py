from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher import State
from aiogram.utils import executor
import app  # app.py dan funksiyalarni chaqirish uchun

# Bot tokenini belgilang
TOKEN = '7781176427:AAHmiWvljlPZAvg9Wy4VvhbzGG9oNfWFQ-s'  # Bot tokenini o'zgartiring
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Davomiylik holatlarini belgilash
class AccountState(State):
    waiting_for_account_info = State()

# /start komandasini qayta ishlash
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Salom! Iltimos, hisob ma'lumotlaringizni yuboring (API ID, API Hash, telefon raqami).")
    await AccountState.waiting_for_account_info.set()  # Davomiylik holatiga o'tish

# Hisob ma'lumotlarini qabul qilish
@dp.message_handler(state=AccountState.waiting_for_account_info, content_types=types.ContentTypes.TEXT)
async def receive_account_info(message: types.Message, state: FSMContext):
    account_info = message.text.split(',')
    
    if len(account_info) != 3:
        await message.reply('Iltimos, hisob ma\'lumotlaringizni to\'g\'ri formatda kiriting: "API ID, API Hash, Telefon raqami".')
        return

    api_id, api_hash, phone_number = [info.strip() for info in account_info]
    app.start_bot(api_id, api_hash, phone_number)  # app.py da funktsiyani chaqirish
    await message.reply('Hisob ma\'lumotlaringiz qabul qilindi! Bot ishga tushmoqda...')

    # Davomiylik holatini tozalash
    await state.finish()

def main():
    # Botni ishga tushirish
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
