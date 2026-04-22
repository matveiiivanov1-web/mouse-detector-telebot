import telebot
from dotenv import load_dotenv
import os
from cv_service import handle_image


load_dotenv()
bot = telebot.TeleBot(os.getenv('TG_API_TOKEN'))

@bot.message_handler(commands=['start'])
def start_command(message):
    text= (
        f'Привет {message.from_user.first_name}!\n\n'
        'Я бот, который распознает мышки на картинках. Просто отправь мне фото мышки, и я скажу, какого типа она!'
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    temp_data = bot.get_file(message.photo[-1].file_id)
    file_name = temp_data.file_path.split('/')[-1]

    downloaded_file = bot.download_file(temp_data.file_path)
    image_path = f'images/{message.message_id}.jpg'
    with open(image_path, 'wb') as image: 
        image.write(downloaded_file)

    result = handle_image(image_path)
    
    response_text = ''
    if len(result) >0:
        response_text = 'Найдены следующие объекты: \n'
        for obj in result:
            response_text += f'Класс: {obj["class"]}, вероятность: {obj["confidence"]}%\n'
        with open('./images' + image_path.split('.')[0] + '_result.jpg', 'rb') as file:
            bot.send_photo(message.chat.id, file, caption=response_text)
    else:
        response_text = 'На изображении не найдено мышек.'
        bot.send_message(message.chat.id, response_text)

    os.remove(image_path) 

bot.infinity_polling()