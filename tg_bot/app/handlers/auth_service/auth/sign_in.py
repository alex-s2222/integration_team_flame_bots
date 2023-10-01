from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from telegram import (
    Update,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup
)

import requests
from loguru import logger
import re
from app.handlers.keyboards import main_menu


URL = 'https://auth-api.test-team-flame.ru/auth/sign-in'

INPUT_EMAIL, INPUT_PASSWORD = range(2)

async def __input_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просим пользователя ввести имя для регистрации"""

    await update.message.reply_text(
        text="Введите email", reply_markup=ReplyKeyboardRemove())
    
    return INPUT_EMAIL


async def __check_email_correct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(email_regex, email) is None:
        await update.message.reply_text(
                            text="ОШИБКА \nВведите коректный email")
        return INPUT_EMAIL
    else:
        logger.info(f'EMAIL {email}')
        user_data = context.user_data
        user_data['email'] = email
        user_data['key_project'] = 1

        await update.message.reply_text(
                            text="Введите пароль")
        
        return INPUT_PASSWORD


async def __check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text

    if len(password) < 6:
        await update.message.reply_text(
                            text="ОШИБКА \nПароль должен быть больше 6 символов")
        return INPUT_PASSWORD
    else:
        user_data = context.user_data
        user_data['password'] = password
        logger.info(user_data)
        response = requests.post(URL, data=user_data)

        if (response.status_code >=200) and (response.status_code < 300):
            
            data = response.json()

            user_data['accessToken'] = data['tokens']['accessToken']['token']
            user_data['refreshToken'] = data['tokens']['refreshToken']['token']
            user_data['id'] = data['user']['id']

            logger.info(user_data)

            markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
            await update.message.reply_text(
                            text="успешно", reply_markup=markup)
            return ConversationHandler.END
        else:
            logger.info(response.text)
            await update.message.reply_text(
                            text="ошибка введите данные заново \nВведите email")
            return INPUT_EMAIL



def sign_in() -> ConversationHandler:

    sign_in_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^▶️Войти в аккаунт▶️$'), __input_email),],
        states={
            INPUT_EMAIL: [
                MessageHandler(filters.TEXT, __check_email_correct),
            ],
            INPUT_PASSWORD: [
                MessageHandler(filters.TEXT, __check_password)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Назад в главное меню$"), ...),
                   ],
    )

    return sign_in_handler