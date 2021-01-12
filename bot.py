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
pd.set_option('display.max_colwidth', -1)
import time
import datetime
from preprocessing import get_grayscale, thresholding
from identify_test import get_tests
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


base_file = 'symptom_check.xlsx'

#TODO Настроить автоматическую загрузку актуальных данных сюда
test_url_dict = pd.read_excel('synonyms_urls.xlsx', engine='openpyxl')

#Config vars
with open('config.json') as f:
 token = json.load(f)

#initialise bot
bot = telebot.TeleBot(token['telegramToken'])

@bot.message_handler(func=lambda message: message.text == "Привет")
def start_message(message):
    sticker = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Распознать направление', 'Проверить симптомы')
    msg = bot.send_message(message.chat.id, 'Чем займемся?', reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Распознать направление', 'Проверить симптомы')
    msg = bot.send_message(message.chat.id, 'Чем займемся?', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Распознать направление")
def what_to_do(message):
    msg = bot.send_message(message.chat.id, "Пришлите фотографию с направлением от врача")
    bot.register_next_step_handler(msg, img2text)



@bot.message_handler(content_types=['photo'])
def img2text(msg):
    
    if msg.text == '/start':
            start_message(msg)
            return

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



def get_recommendation(chat_id):
    base = pd.read_excel(base_file, engine='openpyxl')
    data = pd.read_csv('symptom_log.csv')
    user_line = data.loc[data['ID'] == chat_id]
    user_line = user_line.loc[int(user_line.index.values)]

    recommendation_set = set()

    for question in user_line.keys()[2:]:
        question_list = base.loc[base['QUESTION'] == question]
        answer_list = question_list.loc[question_list['ANSWER'] == user_line[question]]
        answer_list = answer_list.drop(['QUESTION', 'ANSWER', 'ID'], axis=1)
        for vit in answer_list.columns[answer_list.notna().any()].tolist():
            recommendation_set.add(vit)

    answer_string = 'Вам необходимо проверить следующие витамины: \n'
    for vit in recommendation_set:
        answer_string += vit
        answer_string += '\n'

    return answer_string


@bot.message_handler(func=lambda message: message.text == "Проверить симптомы")
def next_symptom1(message):
    chat_id = message.chat.id
    text = message.text

    data = pd.read_csv('symptom_log.csv')
    base = pd.read_excel(base_file, engine='openpyxl')

    if text == '/start':
        question_id = None
        # Обновляем счетчик в таблице
        data.loc[data['ID'] == chat_id, ['question_id']] = question_id

        # Ставим временную отметку
        data.loc[data['ID'] == chat_id, ['Timestamp']] = (datetime.datetime.now()).timestamp()
        data.to_csv('symptom_log.csv', index=False)
        start_message(message)
        return

    # Если под данного юзера еще не заведена строка в таблице, то надо её завести
    if chat_id not in data.ID.values:
        data = data.append({'ID': chat_id}, ignore_index=True)

    # В таблице есть поле question_id - в нем хранится id последнего заданного вопроса
    question_id = data.loc[data['ID'] == chat_id, ['question_id']]

    # Если question_id == Null - значит это самый первый вопрос.
    # В таком случае текущее сообщение от пользователя записывать не надо
    # Но счетчик вопроса надо прибавить
    if (question_id.isna()).loc[int(question_id.index.values), 'question_id']:
        # Записываем, что последний заданный вопрос - 0
        question_id = 0
        data.loc[data['ID'] == chat_id, ['question_id']] = question_id
        data.to_csv('symptom_log.csv', index=False)

        # Вытаскиваем текст вопроса и возможных ответов по question_id
        question = base.loc[base['ID'] == question_id, ['QUESTION']].drop_duplicates()
        question = question['QUESTION'].values[0]
        answers = (base.loc[base['QUESTION'] == question]['ANSWER']).tolist()
        answers = list(set(answers))

        # Задаем вопрос
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row(answers[0], answers[1])

        msg = bot.send_message(message.chat.id, question, reply_markup=keyboard)
        bot.register_next_step_handler(msg, next_symptom1)
    elif question_id.loc[int(question_id.index.values), 'question_id'] > base['ID'].max():

        bot.send_message(chat_id, get_recommendation(chat_id))
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row('Распознать направление', 'Проверить симптомы')
        msg = bot.send_message(message.chat.id, 'Что-нибудь еще?', reply_markup=keyboard)
    else:
        # Если вопрос не первый, то сообщение от пользователя содержит ответ на предыдущий вопрос.
        # question_id этого вопроса на данный момент записан у пользователя
        question_id = question_id.loc[int(question_id.index.values), 'question_id']

        # Получаем текст вопроса по question_id
        question = base.loc[base['ID'] == question_id, ['QUESTION']].drop_duplicates()
        question = question['QUESTION'].values[0]

        # Для данного пользователя добавляем ответ в поле, соответствующее вопросу.
        # Если вопрос еще не был задан, то создаем под него столбец
        try:
            data.loc[data['ID'] == chat_id, [question]] = text

        except:
            data.insert(2, question, None)
            data.loc[data['ID'] == chat_id, [question]] = text

        # Добавляем счетчик вопроса, чтобы теперь задать следующий вопрос
        question_id += 1

        if question_id > base['ID'].max():
            question_id = None
            # Обновляем счетчик в таблице
            data.loc[data['ID'] == chat_id, ['question_id']] = question_id

            # Ставим временную отметку
            data.loc[data['ID'] == chat_id, ['Timestamp']] = (datetime.datetime.now()).timestamp()
            data.to_csv('symptom_log.csv', index=False)

            bot.send_message(chat_id, get_recommendation(chat_id))
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            keyboard.row('Распознать направление', 'Проверить симптомы')
            msg = bot.send_message(message.chat.id, 'Что-нибудь еще?', reply_markup=keyboard)
        else:
            # Обновляем счетчик в таблице
            data.loc[data['ID'] == chat_id, ['question_id']] = question_id

            # Ставим временную отметку - когда вопрос был задан
            data.loc[data['ID'] == chat_id, ['Timestamp']] = (datetime.datetime.now()).timestamp()
            data.to_csv('symptom_log.csv', index=False)

            # Получаем текст и ответы для нового вопроса
            question = base.loc[base['ID'] == question_id, ['QUESTION']].drop_duplicates()
            question = question['QUESTION'].values[0]
            answers = (base.loc[base['QUESTION'] == question]['ANSWER']).tolist()
            answers = list(set(answers))

            # Задаем вопрос и ждем ответ
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            keyboard.row(answers[0], answers[1])

            msg = bot.send_message(message.chat.id, question, reply_markup=keyboard)
            bot.register_next_step_handler(msg, next_symptom1)


# pool~start the bot
bot.infinity_polling(True)