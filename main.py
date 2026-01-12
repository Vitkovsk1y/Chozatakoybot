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

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

r = sr.Recognizer()
   
async def help_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
🆘 *Помощь по использованию бота*

📋 *Основные команды:*
/start - Запустить бота и показать меню
/help - Показать это сообщение
/about - Информация о проекте

🎤 *Как использовать:*
1. Нажмите на иконку микрофона в Telegram
2. Запишите голосовое сообщение (до 5 минут)
3. Отправьте его боту
4. Получите распознанный текст

📁 *Поддерживаемые форматы:*
• Голосовые сообщения
• Аудиофайлы (MP3, WAV, FLAC)

⚙️ *Настройки:*
• Язык распознавания: русский (можно изменить)
• Максимальная длина: 5 минут
• Формат ответа: текст

❗ *Проблемы и решения:*
• *Не распознается речь* - говорите четче и без фонового шума
• *Ошибка при загрузке* - попробуйте отправить файл меньше 20 МБ
• *Долгая обработка* - зависит от длины аудио

📞 *Поддержка:*
Если возникли проблемы, напишите разработчику или создайте issue на GitHub.

👇 *Выберите действие из меню ниже*
    """
    
    # Создаем клавиатуру для удобства
    keyboard = [
        ['🎤 Отправить аудио', '🔙 Назад'],
        ['ℹ️ О проекте', '📊 Статистика']
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    
    await update.message.reply_text(
        help_text, 
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

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






