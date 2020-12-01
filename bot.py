#required packages
import telebot
import requests
import os
import json
import cv2 
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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


# #Intitialize YouTube downloader
# ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

# # works when /ytdl <link> is given
# @bot.message_handler(commands=['ytdl'])
# def down(msg):
#     args = msg.text.split()[1]
#     try:
#         with ydl:
#             result = ydl.extract_info(
#                 args,
#                 download=False  # We just want to extract the info
#             )

#         if 'entries' in result:
#             # Can be a playlist or a list of videos
#             video = result['entries'][0]
#         else:
#             # Just a video
#             video = result
        
#         for i in video['formats']:
#             link = '<a href=\"' + i['url'] + '\">' + 'link' + '</a>'
#             if i.get('format_note'):
#                 bot.reply_to(msg, 'Quality-' + i['format_note'] + ': ' + link, parse_mode='HTML')
#             else:
#                 bot.reply_to(msg, link, parse_mode='HTML', disable_notification=True)
#     except:
#         bot.reply_to(msg, 'This can\'t be downloaded by me')

@bot.message_handler(content_types=['photo'])
def img2text(msg):
    bot.send_message(msg.chat.id, 'message.photo = {}'.format(msg.photo))
    fileID = msg.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(msg, pytesseract.image_to_string('image.jpg', lang="rus+eng"))

    

#pool~start the bot
bot.polling()