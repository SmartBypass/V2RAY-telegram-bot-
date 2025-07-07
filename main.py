import telebot
from web import start
import threading

import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "👋 Bot is working!")

def run_bot():
    bot.polling()

if __name__ == '__main__':
    threading.Thread(target=start).start()
    run_bot()
