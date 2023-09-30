from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from telegram import (
    Update,
    ReplyKeyboardMarkup
)

from app.handlers.keyboards import main_menu

import requests
import re
from loguru import logger



URL = 'https://auth-api.test-team-flame.ru/auth/sign-in'

INPUT_FIRST_NAME, INPUT_LAST_NAME, INPUT_SERNAME, INPUT_EMAIL, INPUT_PASSWORD = range(5)

async def __input_names(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просим пользователя ввести имя для регистрации"""

    await update.message.reply_text(
        text="Введите Имя")
    
    return INPUT_FIRST_NAME


async def __check_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """проверка на корректный ввод имени """
    first_name = update.message.text

    if len(first_name) < 2:
        await update.message.reply_text(
                            text="ОШИБКА \nВведите корректное имя \nИмя должно быть не меньше 2 букв")
        return INPUT_FIRST_NAME
    else:
        logger.info(f'UserName {first_name}')
        user_data = context.user_data
        user_data['firstName'] = first_name

        await update.message.reply_text(
                            text="Введите Фамилию")
        return INPUT_LAST_NAME


async def __check_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_name = update.message.text

    if len(last_name) < 2:
        await update.message.reply_text(
                    text="ОШИБКА \nВведите корректную Фамилию \nФамилия должна быть не меньше 2 букв")
        return INPUT_LAST_NAME
    else:
        logger.info(f'UserLast {last_name}')
        user_data = context.user_data
        user_data['lastName'] = last_name

        await update.message.reply_text(
                            text="Введите Отчество")
        return INPUT_SERNAME


async def __check_ser_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ser_name = update.message.text

    if len(ser_name) < 2:
        await update.message.reply_text(
                    text="ОШИБКА \nВведите корректное Отчество \nОтчество должно быть не меньше 2 букв")
        return INPUT_SERNAME
    else:
        logger.info(f'UserSER {ser_name}')
        user_data = context.user_data
        user_data['surName'] = ser_name

        await update.message.reply_text(
                            text="Введите email")
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
            user_data['id'] = data['id']

            logger.info(user_data)
            markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
            
            await update.message.reply_text(
                            text="успешно", reply_markup=markup)
            return ConversationHandler.END
        else:
            await update.message.reply_text(
                            text="ошибка")
            



def sign_up() -> ConversationHandler:

    sign_up_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🆕Создать аккаунт🆕$'), __input_names),],
        states={
            INPUT_FIRST_NAME: [
                MessageHandler(filters.TEXT, __check_first_name),
            ],
            INPUT_LAST_NAME:[
                MessageHandler(filters.TEXT, __check_last_name),
            ],
            INPUT_SERNAME:[
                MessageHandler(filters.TEXT, __check_ser_name),
            ],
            INPUT_EMAIL: [
                MessageHandler(filters.TEXT, __check_email_correct),
            ],
            INPUT_PASSWORD: [
                MessageHandler(filters.TEXT, __check_password),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Назад в главное меню$"), ...),
                   ],
    )

    return sign_up_handler