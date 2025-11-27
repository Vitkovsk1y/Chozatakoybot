import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import speech_recognition as sr
from pydub import AudioSegment
import os

BOT_TOKEN = '8384769559:AAGUo36O_nH5UsNQ25qHdWL7vXt-9S5cg1o'
LANG_CODE = "ru-RU"
r = sr.Recognizer()

def transcribe_file(file_path: str, file_format: str) -> str:
    wav_path = file_path.rsplit('.', 1)[0] + ".wav"
    try:
        AudioSegment.from_file(file_path, format=file_format).export(wav_path, format="wav")
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio, language=LANG_CODE)
            return text
    except sr.UnknownValueError:
        return "Извините, речь не распознана (возможно, слишком тихо или нет речи)."
    except sr.RequestError:
        return "Ошибка соединения с сервисом распознавания речи (проверьте интернет)."
    except Exception as e:
        print(f"Произошла ошибка при обработке: {e}")
        return f"Произошла внутренняя ошибка при обработке аудио. Возможно, файл в неподдерживаемом формате ({file_format})."
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Отправьте мне голосовое сообщение или аудиофайл (mp3, m4a, wav), и я преобразую его в текст.'
    )

async def audio_transcribe_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.voice:
        file_info = update.message.voice
        file_format = 'ogg'
    elif update.message.audio:
        file_info = update.message.audio
        file_format = file_info.mime_type.split('/')[-1] if file_info.mime_type else 'mp3'
        if file_info.file_name:
            file_format = file_info.file_name.rsplit('.', 1)[-1]
    else:
        await update.message.reply_text("Не могу обработать этот тип сообщения.")
        return
    file_id = file_info.file_id
    new_file = await context.bot.get_file(file_id)
    input_path = f"{file_id}.{file_format}"
    await new_file.download_to_drive(input_path)
    await update.message.reply_text("🗣️ Начинаю распознавание речи...")
    transcribed_text = transcribe_file(input_path, file_format)
    await update.message.reply_text(f"📝 **Распознанный текст**:\n\n{transcribed_text}",
                                    parse_mode=telegram.constants.ParseMode.MARKDOWN)

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.VOICE | filters.AUDIO & ~filters.COMMAND,
        audio_transcribe_handler
    ))
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()