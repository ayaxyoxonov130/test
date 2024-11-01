import telebot
import os
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS

# Bot tokenini kiriting
bot_token = '7781176427:AAHmiWvljlPZAvg9Wy4VvhbzGG9oNfWFQ-s'
bot = telebot.TeleBot(bot_token)

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    # Ovozli xabarni yuklab olish
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Ovozli xabarni saqlash
    with open('voice.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    # Ovozli xabarni .wav formatiga aylantirish
    audio = AudioSegment.from_file('voice.ogg', format='ogg')
    audio.export('voice.wav', format='wav')

    # Ovozli xabarni matnga o‘girish
    recognizer = sr.Recognizer()
    with sr.AudioFile('voice.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='uz-UZ')
            print("Ovozli xabarda aytilgan:", text)
        except sr.UnknownValueError:
            text = "Tushunarsiz xabar"
        except sr.RequestError:
            text = "Xatolik: API bilan muammo yuz berdi"

    # Matnni ovozli javobga aylantirish
    response_text = "Vaalaykum assalom, nima xizmat?"
    tts = gTTS(response_text, lang='uz')
    tts.save('response.ogg')

    # Ovozli javobni foydalanuvchiga yuborish
    with open('response.ogg', 'rb') as audio_response:
        bot.send_voice(message.chat.id, audio_response)

    # Vaqtinchalik fayllarni o‘chirish
    os.remove('voice.ogg')
    os.remove('voice.wav')
    os.remove('response.ogg')

# Botni ishga tushirish
bot.polling()
