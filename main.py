import telebot
from telebot import types
import cv2
import numpy as np
import easyocr

# Создаем экземпляр бота
bot = telebot.TeleBot("6144963851:AAFhbFerKTkfArOixCr8sOGXKHdBcoV19Cc")

# Переменная для хранения пути к загруженному файлу
uploaded_file_path = ""

# Создаем экземпляр easyocr и загружаем модели
reader = easyocr.Reader(['en'])

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем меню
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('/download')
    item2 = types.KeyboardButton('/show')
    item3 = types.KeyboardButton('/help')
    item4 = types.KeyboardButton('exit')
    markup.add(item1, item2, item3, item4)

    # Отправляем приветственное сообщение с меню
    bot.send_message(message.chat.id, "Привет! попробуем угадать текст с картинки только English", reply_markup=markup)

# Обработчик команды /downloadpicture
@bot.message_handler(commands=['download'])
def download_picture(message):
    # Отправляем сообщение с просьбой загрузить файл
    bot.send_message(message.chat.id, "Пожалуйста, загрузите файл с картинкой.")

# Обработчик всех входящих файлов
@bot.message_handler(content_types=['photo', 'document'])
def handle_file(message):
    global uploaded_file_path

    # Проверяем, является ли файл изображением
    if message.photo or (message.document and message.document.mime_type.startswith('image/')):
        # Получаем информацию о файле
        if message.photo:
            file_id = message.photo[-1].file_id
        else:
            file_id = message.document.file_id

        # Загружаем файл
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем файл на диск
        uploaded_file_path = "uploaded_image.jpg"
        with open(uploaded_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Отправляем сообщение с подтверждением загрузки
        bot.send_message(message.chat.id, "Файл успешно загружен.")
    else:
        # Если загруженный файл не является изображением, отправляем сообщение об ошибке
        bot.send_message(message.chat.id, "Пожалуйста, загрузите файл с картинкой.")

# Обработчик команды /showpredict
@bot.message_handler(commands=['show'])
def show_predict(message):
    global uploaded_file_path

    # Проверяем, был ли загружен файл
    if uploaded_file_path:
        # Загружаем изображение с помощью OpenCV
        image = cv2.imread(uploaded_file_path)

        # Преобразуем изображение в оттенки серого
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Распознаем текст с помощью easyocr
        result = reader.readtext(gray)

        # Извлекаем распознанный текст из результата
        recognized_text = [text for (_, text, _) in result]

        # Отправляем каждую распознанную строку отдельным сообщением
        for text in recognized_text:
            bot.send_message(message.chat.id, text)
    else:
        # Если файл не был загружен, отправляем сообщение об ошибке
        bot.send_message(message.chat.id, "Пожалуйста, загрузите файл с картинкой сначала.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def helper(message):
    # Отправляем сообщение помощь
    bot.send_message(message.chat.id, "Запустите бота командой /start или кнопкой меню start\n  - Нажмите кнопку "
                                      "/download выберете фото с текстом на Английском языке и отправьте \n"
                                      "- Нажмите кнопку /show и получите текст из картинки в сообщении\n"
                                      "- Нажмете /help помощь получите ")

# Запускаем бота
bot.polling()
