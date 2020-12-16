# required packages
import telebot
import datetime

import os
import json
import pandas as pd

# Config vars
with open('config.json') as f:
    token = json.load(f)

# initialise bot
bot = telebot.TeleBot(token['telegramToken'])

# @bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == "Проверить симптомы")
def ask_age(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    data = data.append({'ID': chat_id}, ignore_index=True)
    data.to_csv('symptom_log.csv', index=False)
    text = message.text
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('18-30', '30-50', '50+')
    msg = bot.send_message(message.chat.id, 'Сколько вам лет', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_sex)



def ask_sex(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Age']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('М', 'Ж')
    msg = bot.send_message(message.chat.id, 'Какого вы пола?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_preg)

def ask_preg(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Sex']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы беременны, планируете беременность или кормите грудью?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_meno)

def ask_meno(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Pregnancy']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Пре', 'Пост')
    msg = bot.send_message(message.chat.id, 'У вас пре- или постменопауза?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_weight)

def ask_weight(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Meno']] = text
    data.to_csv('symptom_log.csv', index=False)
    msg = bot.send_message(message.chat.id, 'Какой ваш вес?')
    bot.register_next_step_handler(msg, ask_height)

def ask_height(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Weight']] = text
    data.to_csv('symptom_log.csv', index=False)
    msg = bot.send_message(message.chat.id, 'Какой у вас рост?')
    bot.register_next_step_handler(msg, ask_vegan)


def ask_vegan(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Height']] = text
    data.loc[data['ID'] == chat_id, ['IMT']] = data.loc[data['ID'] == chat_id, ['Weight']] / int(text)**2
    data.to_csv('symptom_log.csv', index=False)

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы веган или вегетарианец?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_coffee)


def ask_coffee(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Vegan']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Принимаете ли вы хотя бы чашку кофе, кофеинсодержащего продукта или газировки в день?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_sweet)


def ask_sweet(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Coffee']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы употребляете сладости, такие как печенье, пирожные или мороженое, чаще, чем 2 раза в неделю?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_alcohol)


def ask_alcohol(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Sweet']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы курите или употребляете алкоголь более 2 раз в неделю?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_stress)


def ask_stress(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Alcohol']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы постоянно испытываете от среднего до высокого уровня стресса?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_sport)


def ask_sport(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Stress']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы занимаетесь спортом, по крайней мере, 2-3 раза в неделю?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_travel)


def ask_travel(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Sport']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы выезжаете из страны хотя бы раз в 3 месяца?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_sleep)


def ask_sleep(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Travel']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы спите менее 7 часов в сутки?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_antibiotics)


def ask_antibiotics(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Sleep']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы принимали антибиотики за последние 3 месяца?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_immunity)


def ask_immunity(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Antibiotics']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы легко заболеваете (у вас низкий иммунитет)?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_surgery)

def ask_surgery(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Immunity']] = text
    data.to_csv('symptom_log.csv', index=False)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вам делали какие-либо операции за последние 3 месяца?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_last)


def ask_last(message):
    data = pd.read_csv('symptom_log.csv')
    chat_id = message.chat.id
    text = message.text
    data.loc[data['ID'] == chat_id, ['Surgery']] = text
    data.loc[data['ID'] == chat_id, ['Timestamp']] = (datetime.datetime.now()).timestamp()
    data.to_csv('symptom_log.csv', index=False)
    bot.send_message(chat_id, get_recommendation(chat_id))


def get_recommendation(chat_id):
    base = pd.read_excel('symptom_check.xlsx')
    data = pd.read_csv('symptom_log.csv')
    user_line = data.loc[data['ID'] == chat_id]
    user_line = user_line.loc[user_line['Timestamp'].argmax()]

    recommendation_set = set()

    for question in user_line.keys()[2:]:
        question_list = base.loc[base['QUESTION'] == question]
        answer_list = question_list.loc[question_list['ANSWER'] == user_line[question]]
        answer_list = answer_list.drop(['QUESTION', 'ANSWER'], axis=1)
        for vit in answer_list.columns[answer_list.notna().any()].tolist():
            recommendation_set.add(vit)

    answer_string = 'Вам необходимо проверить следующие витамины: \n'
    for vit in recommendation_set:
        answer_string += vit
        answer_string += '\n'

    return answer_string



# pool~start the bot
bot.infinity_polling(True)