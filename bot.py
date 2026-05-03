import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# تنظیمات لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# توکن ربات خود را اینجا وارد کنید
TOKEN = "8681749773:AAFmxOrklF5ttScmGeqmM-DeOO63QaSy6Sc"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! لینک ویدیوی یوتیوب را برای من بفرستید تا با کیفیت دلخواه دانلود کنم.")

def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    
    # بررسی اینکه آیا لینک یوتیوب است یا خیر
    if "youtube.com" not in url and "youtu.be" not in url:
        update.message.reply_text("لطفاً یک لینک معتبر یوتیوب بفرستید.")
        return

    update.message.reply_text("در حال پردازش... لطفاً صبر کنید.")
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # ارسال فایل به کاربر
            with open(filename, 'rb') as video:
                update.message.reply_video(video)
            
            # حذف فایل پس از ارسال برای صرفه‌جویی در فضا
            os.remove(filename)
            
    except Exception as e:
        logger.error(e)
        update.message.reply_text("متأسفانه خطایی رخ داد. لطفاً لینک را بررسی کنید.")

def main():
    # استفاده از توکن خود
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
