import os
import telebot
from web import start
import threading
import json
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = 'user_data.json'
LINK_FILE = 'links.txt'
ADMIN_ID = 6987095248  

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_today():
    return datetime.utcnow().strftime('%Y-%m-%d')

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "👋 স্বাগতম! আপনি `/getlink` লিখে ফ্রি V2Ray লিংক পেতে পারেন।")

@bot.message_handler(commands=['getlink'])
def get_link(message):
    user_id = str(message.from_user.id)
    data = load_data()
    today = get_today()

    if user_id not in data:
        data[user_id] = {"links": [], "dates": {}}

    today_links = data[user_id]["dates"].get(today, 0)

    if today_links >= 2:
        bot.reply_to(message, "❌ আজকে আপনি ২টি লিংক নিয়ে ফেলেছেন। কালকে আবার চেষ্টা করুন।")
        return

    try:
        with open(LINK_FILE, 'r') as f:
            links = f.read().splitlines()
        if not links:
            bot.reply_to(message, "😥 দুঃখিত, আপাতত কোনো ফ্রি লিংক নেই।")
            return
        link = links.pop(0)
        with open(LINK_FILE, 'w') as f:
            f.write('\n'.join(links))

        data[user_id]["links"].append(link)
        data[user_id]["dates"][today] = today_links + 1
        save_data(data)

        bot.reply_to(message, f"✅ আপনার লিংক:\n`{link}`", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"⚠️ সমস্যা হয়েছে: {e}")

@bot.message_handler(commands=['mylinks'])
def my_links(message):
    user_id = str(message.from_user.id)
    data = load_data()
    links = data.get(user_id, {}).get("links", [])
    if not links:
        bot.reply_to(message, "📭 আপনি এখনো কোনো লিংক নেননি।")
    else:
        bot.reply_to(message, "📦 আপনার লিংকগুলো:\n\n" + '\n'.join(links))

@bot.message_handler(commands=['adminstats'])
def admin_stats(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ আপনি এই কমান্ড ব্যবহার করতে পারেন না।")
        return

    data = load_data()
    report = "📊 ব্যবহারকারীদের লিংক হিসাব:\n\n"
    for uid, info in data.items():
        total = len(info.get("links", []))
        report += f"👤 {uid} → {total} লিংক\n"
    bot.reply_to(message, report)

def run_bot():
    bot.polling()

if __name__ == '__main__':
    threading.Thread(target=start).start()
    run_bot()
