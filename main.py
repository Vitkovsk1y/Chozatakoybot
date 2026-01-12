import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import speech_recognition as sr

# Загружаем токен из файла
with open('token.txt', 'r') as f:
    BOT_TOKEN = f.read().strip()

r = sr.Recognizer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Отправьте голосовое сообщение для распознавания.')

async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.voice:
        await update.message.reply_text("Распознаю...")

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, audio_handler))

    print("Бот запущен...")
    application.run_polling()


if __name__ == '__main__':
    main()
if __name__ == '__main__':

    main()


