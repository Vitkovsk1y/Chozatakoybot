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

# Настройка централизованного логирования
def setup_logging():
    """Настройка системы логирования с ротацией файлов"""
    # Создаем логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Форматтер для логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Файловый обработчик с ротацией (макс 5 файлов по 10 МБ каждый)
    file_handler = RotatingFileHandler(
        'bot.log',
        maxBytes=10*1024*1024,  # 10 МБ
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Инициализация логгера
logger = setup_logging()

class ErrorHandler:
    """Класс для централизованной обработки ошибок"""
    
    @staticmethod
    def log_error(error: Exception, context: Optional[dict] = None) -> None:
        """
        Логирование ошибок с контекстом
        
        Args:
            error: Исключение
            context: Дополнительный контекст ошибки
        """
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc()
        }
        
        if context:
            error_data['context'] = context
        
        # Логируем в файл
        logger.error(json.dumps(error_data, ensure_ascii=False))
        
        # Также логируем в консоль для отладки
        logger.error(f"Error: {error}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    
    @staticmethod
    async def send_error_to_user(update: Update, error_message: str) -> None:
        """Отправка пользователю сообщения об ошибке"""
        try:
            user_friendly_message = (
                "❌ Произошла ошибка при обработке вашего запроса. "
                "Попробуйте еще раз или обратитесь в поддержку."
            )
            await update.message.reply_text(user_friendly_message)
        except Exception as e:
            logger.error(f"Failed to send error message to user: {e}")

# Декоратор для обработки ошибок в асинхронных функциях
def error_handler_async(func):
    """Декоратор для автоматической обработки ошибок в асинхронных функциях"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Извлекаем update из аргументов
            update = None
            for arg in args:
                if isinstance(arg, Update):
                    update = arg
                    break
            
            context_data = {
                'function': func.__name__,
                'args': str(args),
                'kwargs': str(kwargs)
            }
            
            ErrorHandler.log_error(e, context_data)
            
            if update:
                await ErrorHandler.send_error_to_user(update, str(e))
            
            return None
    return wrapper

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
    main()





