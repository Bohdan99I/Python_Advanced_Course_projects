"""Telegram бот для прогнозу погоди."""
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from weather_service import get_weather

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """Обробник команди /start."""
    await update.message.reply_text(
        'Привіт! Я бот прогнозу погоди.\n'
        'Надішліть мені назву міста, і я покажу поточну погоду.\n'
        'Наприклад: Київ, Львів, Одеса'
    )

async def help_command(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """Обробник команди /help."""
    await update.message.reply_text(
        'Доступні команди:\n'
        '/start - Початок роботи\n'
        '/help - Довідка\n\n'
        'Просто надішліть назву міста для отримання прогнозу погоди.'
    )

async def get_weather_handler(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """Обробник текстових повідомлень з назвою міста."""
    city = update.message.text.strip()

    if not city:
        await update.message.reply_text('Будь ласка, введіть назву міста.')
        return

    await update.message.reply_text(f'Отримую дані про погоду в місті {city}...')

    weather_data = get_weather(city)

    if weather_data.get('error'):
        await update.message.reply_text(f"❌ Помилка: {weather_data['error']}")
    else:
        message = (
            f"🌍 Погода в місті {weather_data['city']}, {weather_data['country']}\n\n"
            f"🌡 Температура: {weather_data['temperature']}°C\n"
            f"🤔 Відчувається як: {weather_data['feels_like']}°C\n"
            f"☁️ Опис: {weather_data['description']}\n"
            f"💧 Вологість: {weather_data['humidity']}%\n"
            f"💨 Швидкість вітру: {weather_data['wind_speed']} м/с\n"
            f"🔽 Тиск: {weather_data['pressure']} гПа"
        )
        await update.message.reply_text(message)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробник помилок."""
    logger.error('Update %s caused error %s', update, context.error)

def main():
    """Головна функція для запуску бота."""
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not telegram_token:
        logger.error('TELEGRAM_BOT_TOKEN не знайдено в .env файлі')
        return

    application = Application.builder().token(telegram_token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather_handler))

    application.add_error_handler(error_handler)

    logger.info('Бот запущено...')
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
