#required packages
import telebot
import requests
import os
import json
import cv2 
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt
import pandas as pd
import time
from preprocessing import get_grayscale, thresholding
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#TODO Настроить автоматическую загрузку актуальных данных сюда
test_url_dict = pd.read_csv('test_url_dict.csv')

#Config vars
with open('config.json') as f:
 token = json.load(f)

#initialise bot
bot = telebot.TeleBot(token['telegramToken'])
x = bot.get_me()
print(x)

#handling commands - /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome user")

#handling commands - /motivate
@bot.message_handler(commands=['motivate'])
def send_quotes(message):
    quote= requests.request(url='https://api.quotable.io/random',method='get')
    bot.reply_to(message, quote.json()['content'])


@bot.message_handler(content_types=['photo'])
def img2text(msg):
    # bot.send_message(msg.chat.id, 'message.photo = {}'.format(msg.photo))
    fileID = msg.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    # bot.reply_to(msg, pytesseract.image_to_string('image.jpg', lang="rus+eng"))

    # TODO Поэкспериментировать с другим препроцессингом
    image = cv2.imread('image.jpg')
    gray = get_grayscale(image)
    thresh = thresholding(gray)
    parsed_image = pytesseract.image_to_string(thresh, lang="rus+eng")
    for test in test_url_dict['TEST_NAME']:
        if parsed_image.find(test) >= 0:
            bot.send_message(msg.chat.id, test_url_dict.loc[test_url_dict['TEST_NAME'] == test]['URL'].to_string(index=False))
            time.sleep(0.5)
    bot.send_message(msg.chat.id, "Это всё, что я нашел по этому направлению")

    

#pool~start the bot
bot.polling()