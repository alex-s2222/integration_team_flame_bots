from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler
)

from telegram import (
    Update,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)

from app.handlers.service import keyboards
from app.handlers.service.keyboards import back_to_menu
from app.handlers.keyboards import main_menu
from app.handlers.service import action_space

from loguru import logger
import re


SPACES, ACTION, INPUT_NAME_FOR_SPACE = range(3)


async def __user_spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''пользователь выбирает пространство'''
    await update.message.reply_text(text='Переход в пространства', reply_markup=back_to_menu)
    
    user_data = context.user_data

    markup = InlineKeyboardMarkup(keyboards.create_spaces_keyboard(user_data['accessToken']))

    await update.message.reply_text(
        text="Выберете пространство для выбора действия", reply_markup=markup
    )
    
    return SPACES 


async def __choice_spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''пользователь выбирает действие'''
    # получаем выбор пользователя
    query = update.callback_query
    await query.answer()
    index_spaces = int(query.data)
    logger.info(index_spaces)

    #заносим выбор пользователя в context
    user_data = context.user_data
    user_data['user_choice'] = index_spaces

    markup = InlineKeyboardMarkup(keyboards.spaces_menu_keyboard)

    await query.edit_message_text(
        text="Выберете действия c пространства ", reply_markup=markup
    )

    return ACTION


async def __delete_spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''удаляем пространство'''
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    index_spaces = user_data['user_choice']
    token = user_data['accessToken']
    spaces = action_space.get_user_spaces(token)

    #получаем id пространсва 
    space_id = list(spaces.keys())[index_spaces]

    #удаляем пространсво
    err = action_space.delete_user_space(TOKEN=token, space_id=space_id)

    markup = InlineKeyboardMarkup(keyboards.create_spaces_keyboard(user_data['accessToken']))

    if err:
       await query.edit_message_text(
                            text="ОШИБКА \nВыберете пространство для продолжения", reply_markup=markup)
       return SPACES
    else:
        await query.edit_message_text(
                            text="Пространство удаленно \nВыберете пространство для продолжения", reply_markup=markup)
        return SPACES


async def __get_name_for_create_spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''получаем имя пространства'''
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="введите имя задачи")
    return INPUT_NAME_FOR_SPACE


async def __create_space(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''создаем пространство'''
    user_data = context.user_data

    space_name = update.message.text
    token = user_data['accessToken']


    err = action_space.create_user_space(TOKEN=token, space_name=space_name)
    
    markup = InlineKeyboardMarkup(keyboards.create_spaces_keyboard(user_data['accessToken']))
    if err:
       await update.message.reply_text(
                            text="ОШИБКА \nВведите другое имя для пространства", reply_markup=markup)
       return SPACES
    else:
        await update.message.reply_text(
                            text="Пространство созданно \nВыберете пространство для продолжения", reply_markup=markup)
        return SPACES




async def __back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """выводим клавиатуру меню и завершаем диалог"""
    markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text(text='Переход в главное меню', reply_markup=markup)
    return ConversationHandler.END


def get_spaces() -> ConversationHandler:
    ONE, TWO, THREE, FOUR = range(4)


    spaces_handler= ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Мои пространства$'), __user_spaces),],
        states={
            SPACES: [
                CallbackQueryHandler(__choice_spaces)
            ],
            ACTION:[
                CallbackQueryHandler(__get_name_for_create_spaces,  pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__delete_spaces,  pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(...,  pattern="^" + str(THREE) + "$")
            ],
            INPUT_NAME_FOR_SPACE:[
                MessageHandler(filters.TEXT, __create_space)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Назад в главное меню$"), __back_to_main_menu),
                   ],
    )

    return spaces_handler