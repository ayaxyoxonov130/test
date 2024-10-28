from pyrogram import Client, filters
import os
import asyncio

# Kalit so'zlar faylining nomi
keyword_file = 'keyWord.txt'

# Xabarni yuborish kerak bo'lgan guruh ID'si
target_group_id = -10012345678  # Xabar yuboriladigan guruh ID

# Kalit so'zlar ro'yxatini yuklash funksiyasi
def load_keywords():
    if not os.path.exists(keyword_file):
        return []
    with open(keyword_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

# Yangi kalit so'zlarni faylga qo'shish funksiyasi
def add_keyword(new_keyword):
    with open(keyword_file, 'a', encoding='utf-8') as f:
        f.write(f'{new_keyword}\n')

# Pyrogram mijozini yaratish
app = None

async def start_bot(api_id, api_hash, phone_number):
    global app
    app = Client("my_bot", api_id=api_id, api_hash=api_hash, phone_number=phone_number)

    @app.on_message(filters.text)
    async def text_handler(client, message):
        # Xabar matni
        message_text = message.text

        # Kalit so'zlarni yuklash
        keywords = load_keywords()

        # Agar kalit so'zlardan biri xabar matnida mavjud bo'lsa
        if any(keyword.lower() in message_text.lower() for keyword in keywords):
            print(f"Kalit so'z topildi! Guruh ID: {message.chat.id}")

            # Xabarni boshqa guruhga yuborish
            await client.send_message(target_group_id, f"Yangi xabar: {message_text}")

        # Yangi kalit so'z qo'shish buyrug'i (masalan: /addword yangi_soz)
        if message_text.startswith('/addword'):
            # Buyruqdan so'nggi so'zni ajratib olish
            new_word = message_text.split(' ', 1)[1]
            add_keyword(new_word)
            await message.reply_text(f'Yangi kalit soʻz "{new_word}" qoʻshildi!')

    @app.on_message(filters.voice)
    async def voice_handler(client, message):
        # Ovozli xabarni boshqa guruhga yuborish
        await client.send_message(target_group_id, "Yangi ovozli xabar!")
        await client.send_voice(target_group_id, message.voice.file_id)
        print(f"Ovozli xabar yuborildi! Guruh ID: {message.chat.id}")

    await app.start()  # Botni ishga tushirish
    print("Bot ishga tushdi!")
    await app.idle()  # Bot ishda qoladi

# async funktsiyani qo'llab-quvvatlash uchun asyncio yordamida ishga tushirish
if __name__ == '__main__':
    asyncio.run(start_bot(api_id='', api_hash='', phone_number=''))  # boshlanishda hech qanday hisob ma'lumotlari yo'q
