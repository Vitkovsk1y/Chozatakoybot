import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import speech_recognition as sr
from telegram import ReplyKeyboardMarkup
import os
from dotenv import load_dotenv

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сохраняем выбранный режим в context.user_data"""
    selected_mode = update.message.text
    context.user_data['mode'] = selected_mode
    await update.message.reply_text(f'✅ Режим изменен на: **{selected_mode}**', parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Устанавливаем режим по умолчанию, если его нет
    if 'mode' not in context.user_data:
        context.user_data['mode'] = MODE_TRANSCRIPTION

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


# Константы для режимов
MODE_TRANSCRIPTION = "Расшифровка"
MODE_SUMMARY = "Пересказ"

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
    mode = context.user_data.get('mode', MODE_TRANSCRIPTION)
    if mode == MODE_TRANSCRIPTION:
        await update.message.reply_text("Выбрана расшифровка...")
    else:
        await update.message.reply_text("Выбран пересказ...")
    file_info = update.message.voice or update.message.audio
    new_file = await context.bot.get_file(file_info.file_id)
    
    ext = "ogg" if update.message.voice else "mp3"
    local_path = f"{file_info.file_id}.{ext}"
    
    await new_file.download_to_drive(local_path)
    await update.message.reply_text("📥 Файл успешно скачан на сервер!")
    return local_path


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    
    # Регистрация переключателя режимов (фильтруем текст по названиям кнопок)
    application.add_handler(MessageHandler(
        filters.Text([MODE_TRANSCRIPTION, MODE_SUMMARY]), set_mode
    ))
    
    # Регистрация обработки аудио и текста "Помощь"
    application.add_handler(MessageHandler(filters.Text(['Помощь']), help_button))
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, audio_handler))

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()







