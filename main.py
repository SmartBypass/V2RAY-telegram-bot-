import telebot
from web import start
import threading

BOT_TOKEN = '7548863319:AAH07TxgnYBygfAv5zo0lSks1YpK24bs1k0'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "👋 Bot is working!")

def run_bot():
    bot.polling()

if __name__ == '__main__':
    threading.Thread(target=start).start()
    run_bot()
