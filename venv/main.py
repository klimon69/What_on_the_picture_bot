
#сайт с прокси  https://hidemy.name/ru/proxy-list/?type=h#list
#https://github.com/OlafenwaMoses/ImageAI/tree/master/imageai/Detection
#https://imageai.readthedocs.io/en/latest/

import os
import telebot
from telebot import apihelper
from imageai.Detection import ObjectDetection

apihelper.proxy = {'https':'http://96.96.10.6:3128'}

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я умею распознавать предметы на картинке. Пришли мне фото(КАК ФАЙЛ) и я поищу на нём что-нибудь.')


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        #проверям есть ли такой файл и удаляем его

        filePath = 'C:\Development\what_on_the_picture_bot/venv/objects.jpg';

        # As file at filePath is deleted now, so we should check if file exists or not not before deleting them
        if os.path.exists(filePath):
            os.remove(filePath)
            print("Old file deleted")
        else:
            print("Can not delete the file as it doesn't exists")

        #сохраняем файл
        src = 'C:\Development\what_on_the_picture_bot/venv/objects.jpg'# + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Обрабатываю...")
        print("New file downloaded")


        try:
            exec_path = os.getcwd()

            detector = ObjectDetection()
            detector.setModelTypeAsRetinaNet()
            detector.setModelPath(os.path.join(exec_path, "resnet50_coco_best_v2.0.1.h5"))

            detector.loadModel()

            list = detector.detectObjectsFromImage(input_image=os.path.join(exec_path, "objects.jpg"),
                                                   output_image_path=os.path.join(exec_path, "new_objects.jpg"),
                                                   minimum_percentage_probability=50)
        except Exception as e:
            bot.reply_to(message, "Ошибка в модели - " + e)

        #Отправляем обработанное фото
        photo = 'C:\Development\what_on_the_picture_bot/venv/new_objects.jpg'

        bot.send_photo(message.chat.id, open(photo, 'rb'))

    except Exception as e:
        bot.reply_to(message, "Ой, возникла ошибка. Попробуйте ещё раз.")

bot.polling()