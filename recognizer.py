#required packages
import telebot
import re
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
from identify_test import get_tests
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#TODO Настроить автоматическую загрузку актуальных данных сюда
test_url_dict = pd.read_excel('synonyms_urls.xlsx')

#Config vars
with open('config.json') as f:
 token = json.load(f)

#initialise bot
bot = telebot.TeleBot(token['telegramToken'])

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

    result = get_tests(parsed_image, test_url_dict)

    for url in result['URL']:
        bot.send_message(msg.chat.id, url)
        time.sleep(0.5)
    bot.send_message(msg.chat.id, "Это всё, что я нашел по этому направлению")

@bot.message_handler(content_types=['text'])
def text2text(msg):
    bot.send_message(msg.chat.id, "Начал смотреть")
    result = get_tests(msg.text, test_url_dict)

    for url in result['URL']:
        bot.send_message(msg.chat.id, url)
        time.sleep(0.5)
    bot.send_message(msg.chat.id, "Это всё, что я нашел по этому направлению")