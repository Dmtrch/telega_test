import os
import telebot
import speech_recognition as sr
from pydub import AudioSegment

# Создание экземпляра бота
bot = telebot.TeleBot('6064128961:AAGigUpInPOnKJ8ThHAbq47rakXaFsI4VAI')


# Обработчик сообщений с цифрой от 0 до 10
@bot.message_handler(func=lambda message: message.text.isdigit() and int(message.text) >= 0 and int(message.text) <= 10)
def handle_rating(message):
    bot.send_message(message.chat.id, "Введите оценку от 0 до 10:")
    bot.register_next_step_handler(message, get_rating)

def get_rating(message):
    number = int(message.text)
    bot.send_message(message.chat.id, f"Вы отправили оценку: {number}")
    return str(number)


# Обработчик сообщений с цифрой от 0 до 10
#@bot.message_handler(
#    func=lambda message: message.text.isdigit() and int(message.text) >= 0 and int(message.text) <= 10)
#def get_rating(message):
#    number = int(message.text)
#    bot.send_message(message.chat.id,"введите оценку от 0 до 10")
#    bot.send_message(message.chat.id, f"Вы отправили цифру: {number}")
#    return str(number)

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    chat_id = message.chat.id
    voice = message.voice

    # Проверка наличия папки с именем чата
    chat_folder = str(chat_id)
    if not os.path.exists(chat_folder):
        os.makedirs(chat_folder)

      # Сохранение голосового сообщения в формате OGG
    voice_file_path = f"{chat_folder}/{voice.file_id}.ogg"
    voice_file = bot.get_file(voice.file_id)
    downloaded_file = bot.download_file(voice_file.file_path)

    with open(voice_file_path, 'wb') as new_file:
        new_file.write(downloaded_file)


    # Конвертация голосового сообщения из OGG в WAV
    wav_file_path = f"{chat_folder}/{voice.file_id}.wav"

    with open(wav_file_path,'wb') as converted_file:
        audio_segment = AudioSegment.from_file(voice_file_path, format='ogg')
        audio_segment.export(converted_file, format='wav')


    # Конвертация голосового сообщения в текст
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.listen(source)
        text = recognizer.recognize_google(audio_data, language='ru')

    # Отправка текстового сообщения в чат
    #with open(text_file_path, 'r', encoding='utf-8') as text_file:
    bot.send_message(chat_id, text)

    # Сохранение текстового сообщения в формате TXT
    text_file_path = f"{chat_folder}/{voice.file_id}.txt"
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        # Запись оценки в начало файла текстового сообщения

        rating = get_rating(message)
        text_with_rating = f"Оценка: {rating}\n{text}"

        #text_with_rating = f"Оценка: {get_rating(message)}\n{text}"
        text_file.write(text_with_rating)


# Запуск бота
bot.polling()
