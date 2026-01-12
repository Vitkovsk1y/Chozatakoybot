import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import speech_recognition as sr
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

r = sr.Recognizer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Отправьте голосовое сообщение для распознавания.')

async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file_info = update.message.voice or update.message.audio
    new_file = await context.bot.get_file(file_info.file_id)
    
    ext = "ogg" if update.message.voice else "mp3"
    local_path = f"{file_info.file_id}.{ext}"
    
    await new_file.download_to_drive(local_path)
    await update.message.reply_text("📥 Файл успешно скачан на сервер!")
    return local_path


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, audio_handler))

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()




