import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import speech_recognition as sr
from telegram import ReplyKeyboardMarkup
import os
from dotenv import load_dotenv

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [['Помощь'], ['О проекте']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Привет! Я бот Спринта №2. Пришли аудио.', reply_markup=reply_markup)

    # Создаем клавиатуру с выбором режима
    keyboard = [
        [MODE_TRANSCRIPTION, MODE_SUMMARY],
        ['Помощь', 'О проекте']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    current_mode = context.user_data['mode']
    await update.message.reply_text(
        f'Привет! Текущий режим: **{current_mode}**.\n'
        'Пришли мне голосовое сообщение или смени режим кнопкой ниже.',
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Константы для режимов
MODE_TRANSCRIPTION = "Расшифровка"
MODE_SUMMARY = "Пересказ"

r = sr.Recognizer()
   

async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.voice:
        await update.message.reply_text("Распознаю...")

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    import os
import speech_recognition as sr
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Константы для режимов
MODE_TRANSCRIPTION = "Расшифровка"
MODE_SUMMARY = "Пересказ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Устанавливаем режим по умолчанию, если он еще не выбран
    if 'mode' not in context.user_data:
        context.user_data['mode'] = MODE_TRANSCRIPTION

    # Создаем клавиатуру с выбором режима
    keyboard = [
        [MODE_TRANSCRIPTION, MODE_SUMMARY],
        ['Помощь', 'О проекте']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    current_mode = context.user_data['mode']
    await update.message.reply_text(
        f'Привет! Текущий режим: **{current_mode}**.\n'
        'Пришли мне голосовое сообщение или смени режим кнопкой ниже.',
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатия на кнопки смены режима"""
    selected_mode = update.message.text
    context.user_data['mode'] = selected_mode
    await update.message.reply_text(f"Режим изменен на: **{selected_mode}**", parse_mode='Markdown')

async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Извлекаем текущий режим из контекста
    mode = context.user_data.get('mode', MODE_TRANSCRIPTION)
    
    if update.message.voice:
        if mode == MODE_TRANSCRIPTION:
            await update.message.reply_text("🎙 Начинаю расшифровку аудио...")
            # Здесь будет ваша логика распознавания (Speech-to-Text)
        else:
            await update.message.reply_text("📝 Начинаю делать пересказ (summary)...")
            # Здесь будет логика расшифровки + суммаризации (например, через OpenAI/GigaChat)

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    
    # Обработка текстовых кнопок для смены режима
    application.add_handler(MessageHandler(
        filters.Text([MODE_TRANSCRIPTION, MODE_SUMMARY]), set_mode
    ))
    
    application.add_handler(MessageHandler(filters.VOICE, audio_handler))

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
    application.add_handler(MessageHandler(filters.VOICE, audio_handler))

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()






