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
        file_info = update.message.voice
        file_id = file_info.file_id
        new_file = await context.bot.get_file(file_id)

        await update.message.reply_text("Распознаю...")

        with sr.AudioFile(await new_file.download_as_bytearray()) as source:
            audio = r.record(source)
            text = r.recognize_google(audio, language="ru-RU")
            await update.message.reply_text(text)


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

