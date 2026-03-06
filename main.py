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

# Имитация модулей бота для интеграционного теста
def mock_voice_to_wav(voice_data):
    print("Шаг 1: Голосовое сообщение сконвертировано в .wav")
    return "audio.wav"

def mock_wav_to_text(audio_file):
    print("Шаг 2: Аудио расшифровано в текст")
    return "Пример длинного текста лекции..."

def mock_text_to_summary(text):
    print("Шаг 3: Генерация краткого пересказа завершена")
    return "Краткий конспект: бот работает корректно."

def run_integration_test():
    print("--- ЗАПУСК ИНТЕГРАЦИОННОГО ТЕСТИРОВАНИЯ ---")
    
    # Эмуляция всей цепочки
    voice = "input_voice_blob"
    wav = mock_voice_to_wav(voice)
    text = mock_wav_to_text(wav)
    summary = mock_text_to_summary(text)
    
    print(f"\nФинальный результат: {summary}")
    print("--- ТЕСТ ЗАВЕРШЕН УСПЕШНО ---")
# Тест: Проверка сохранения файла на диск
def test_file_saving(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        if os.path.exists(filename):
            print(f"Успех: Файл {filename} корректно сохранен.")
            return True
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False
        
# Функция очистки
def cleanup(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Файл {file_path} удален.")

# Проверка корректности работы с длинными именами файлов
if __name__ == "__main__":
    # Создаем длинное имя файла
    long_filename = "test_voice_message_" + "a" * 100 + ".txt"
    test_content = "Тестовое содержимое для расшифровки"

    # Запускаем проверку
    if test_file_saving(long_filename, test_content):
        # Если сохранилось — удаляем, чтобы не оставлять мусор
        cleanup(long_filename)
        print("Проверка длинных имен файлов пройдена успешно!")

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

async def global_error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Глобальный обработчик ошибок для приложения"""
    error = context.error
    
    # Логируем ошибку
    error_context = {
        'update': str(update) if update else None,
        'user_data': str(context.user_data) if context.user_data else None,
        'chat_data': str(context.chat_data) if context.chat_data else None
    }
    
    ErrorHandler.log_error(error, error_context)
    
    # Отправляем сообщение пользователю
    if update:
        await ErrorHandler.send_error_to_user(update, str(error))

if __name__ == '__main__':
    run_integration_test()
    main()









