from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import app  # app.py dan funksiyalarni chaqirish uchun

# /start komandasini qayta ishlash
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Salom! Iltimos, hisob ma\'lumotlaringizni yuboring (API ID, API Hash, telefon raqami).')

# Hisob ma'lumotlarini qabul qilish
def receive_account_info(update: Update, context: CallbackContext) -> None:
    account_info = update.message.text.split(',')
    
    if len(account_info) != 3:
        update.message.reply_text('Iltimos, hisob ma\'lumotlaringizni to\'g\'ri formatda kiriting: "API ID, API Hash, Telefon raqami".')
        return

    api_id, api_hash, phone_number = [info.strip() for info in account_info]
    app.start_bot(api_id, api_hash, phone_number)  # app.py da funktsiyani chaqirish
    update.message.reply_text('Hisob ma\'lumotlaringiz qabul qilindi! Bot ishga tushmoqda...')

def main():
    # Telegram bot tokenini o'zgaruvchi sifatida belgilang
    TOKEN = '7781176427:AAHmiWvljlPZAvg9Wy4VvhbzGG9oNfWFQ-s'

    # Updater va Dispatcher ni yaratish
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Handlerlarni qo'shish
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_account_info))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
