import os
import telebot

API_KEY = '5868770569:AAFJcPmA4ZCDv6AVCFXNRYt6GM-iBr_at7A'
#API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['Greet'])
def greet(message):
  bot.reply_to(message, "Hey! How it going?")


@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "hello-test")


bot.infinity_polling()