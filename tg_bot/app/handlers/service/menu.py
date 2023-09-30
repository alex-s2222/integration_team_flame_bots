from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext
)

from telegram import (
    Update,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup
)

from app.handlers.service import keyboards
import requests
from loguru import logger
import re


SPACES = range(1)




async def __user_spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup(keyboards.spaces_menu_keyboard)

    await update.message.reply_text(
        text="Выберете Действие с пространством", reply_markup=markup)
    
    return
    



def sign_up() -> ConversationHandler:

    sign_up_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Мои пространства$'), __user_spaces),],
        states={
            SPACES: [
                CallbackContext(filters.TEXT, __check_email_correct),
            ],
            INPUT_PASSWORD: [
                MessageHandler(filters.TEXT, __check_password),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Назад в главное меню$"), ...),
                   ],
    )

    return sign_up_handler