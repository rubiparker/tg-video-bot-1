import telebot
import yt_dlp
import os

# Токен берём из настроек сервера (на Render мы его добавим)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Кинь ссылку на видео — скачаю и пришлю.")

@bot.message_handler(func=lambda message: message.text and message.text.startswith('http'))
def download_video(message):
    url = message.text.strip()
    status = bot.reply_to(message, "⏳ Скачиваю...")

    ydl_opts = {
        'format': 'best[ext=mp4][filesize<50M]/best[ext=mp4]/best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }

    path = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)

        with open(path, 'rb') as video:
            bot.send_video(message.chat.id, video)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")
    finally:
        if path and os.path.exists(path):
            os.remove(path)
        bot.delete_message(message.chat.id, status.message_id)

print("Бот запущен")
bot.polling(none_stop=True)
