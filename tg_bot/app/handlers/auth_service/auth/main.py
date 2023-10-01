from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)


first_menu = [
    ["▶️Войти в аккаунт▶️", "🆕Создать аккаунт🆕"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """выводим выбор входа в аккаунт"""
    murkup = ReplyKeyboardMarkup(first_menu, resize_keyboard=True,one_time_keyboard=True)
    await update.message.reply_text(
        'Добро пожаловать в интеграцию мессенджера с teamflame, выберете действие', reply_markup=murkup)
    