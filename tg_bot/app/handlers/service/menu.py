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
from app.handlers.service import action_project
from app.handlers.service import action_board
from app.handlers.service import action_columns
from app.handlers.service import action_task

from loguru import logger
import re


SPACES, ACTION_SPACE, INPUT_NAME_FOR_SPACE,\
    INPUT_NAME_FOR_PROJECT, ACTION_PROJECT, PROJECT,\
        BOARD, ACTION_BOARD, INPUT_NAME_FOR_BOARD,\
             COLUMN, ACTION_COLUMN, INPUT_NAME_FOR_COLUMN,\
                TASK, ACTION_TASK, INPUT_NAME_FOR_TASK = range(15)


async def __user_spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''пользователь выбирает пространство'''
    await update.message.reply_text(text='Переход в пространства', reply_markup=back_to_menu)
    
    user_data = context.user_data

    markup = InlineKeyboardMarkup(keyboards.create_spaces_keyboard(user_data['accessToken']))

    await update.message.reply_text(
        text="Создайте или выберите пространство", reply_markup=markup
    )
    
    return SPACES 


async def __choice_spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''пользователь выбирает пространство'''
    # получаем выбор пользователя
    query = update.callback_query
    await query.answer()
    index_spaces = int(query.data) - 1
    logger.info(index_spaces)

    #заносим выбор пользователя в context
    user_data = context.user_data
    token = user_data['accessToken']

    # получаем заносим выбранного пространства
    spaces = action_space.get_user_spaces(token)
    space_id = list(spaces.keys())[index_spaces]
    user_data['space_id'] = space_id
    
    markup = InlineKeyboardMarkup(keyboards.spaces_menu_keyboard)

    await query.edit_message_text(
        text="Выберите действия c пространством", reply_markup=markup
    )

    return ACTION_SPACE


async def __delete_spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''удаляем пространство'''
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    
    token = user_data['accessToken']
    space_id = user_data['space_id']

    #удаляем пространсво
    err = action_space.delete_user_space(TOKEN=token, space_id=space_id)

    markup = InlineKeyboardMarkup(keyboards.create_spaces_keyboard(user_data['accessToken']))

    if err:
       await query.edit_message_text(
                            text="ОШИБКА \nСоздайте или выберите пространство для продолжения", reply_markup=markup)
       return SPACES
    else:
        await query.edit_message_text(
                            text="Пространство удаленно \nСоздайте или выберите пространство для продолжения", reply_markup=markup)
        return SPACES


async def __get_name_for_create_spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''получаем имя пространства'''
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Введите имя пространства")
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
                            text="ОШИБКА \nСоздайте или выберите пространство для продолжения", reply_markup=markup)
       return SPACES
    else:
        await update.message.reply_text(
                            text="Пространство созданно \nСоздайте или выберите пространство для продолжения", reply_markup=markup)
        return SPACES




async def __back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """выводим клавиатуру меню и завершаем диалог"""
    markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text(text='Переход в главное меню', reply_markup=markup)
    return ConversationHandler.END 


# ------------------project-----------------

async def __back_to_space(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_data = context.user_data

    markup = InlineKeyboardMarkup(keyboards.create_spaces_keyboard(user_data['accessToken']))

    await query.edit_message_text(
        text="Создайте или выберите пространство", reply_markup=markup
    )
    
    return SPACES 


async def __go_to_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()


    user_data = context.user_data
    token = user_data['accessToken']
    space_id = user_data['space_id']

    markup = InlineKeyboardMarkup(keyboards.create_projects_keyboard(token, space_id))

    await query.edit_message_text(
            text="Создайте или выберите проект", reply_markup=markup)
    
    return PROJECT
    

async def __choice_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''пользователь выбирает проект '''
    # получаем выбор пользователя
    query = update.callback_query
    await query.answer()
    index_project = int(query.data) - 2
    logger.info(index_project)

    #заносим выбор пользователя в context
    user_data = context.user_data
    token = user_data['accessToken']
    space_id = user_data['space_id']

    # получаем заносим выбранного пространства
    projects = action_project.get_projects(token, space_id)
    project_id = list(projects.keys())[index_project]
    user_data['project_id'] = project_id
    
    markup = InlineKeyboardMarkup(keyboards.project_menu_keyboard)

    await query.edit_message_text(
        text="Выберите действия c проектом ", reply_markup=markup
    )

    return ACTION_PROJECT


async def __get_name_for_create_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''получаем имя для проекта'''
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Введите имя проекта")
    return INPUT_NAME_FOR_PROJECT


async def __delete_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    
    token = user_data['accessToken']
    space_id = user_data['space_id']
    project_id = user_data['project_id']

    #удаляем проект
    err = action_project.delete_project(TOKEN=token, space_id=space_id, project_id=project_id)

    markup = InlineKeyboardMarkup(keyboards.create_projects_keyboard(TOKEN=token, space_id=space_id))

    if err:
       await query.edit_message_text(
                            text="ОШИБКА \nСоздайте или выберите проект для продолжения", reply_markup=markup)
       return PROJECT
    else:
        await query.edit_message_text(
                            text="Пространство удаленно \nСоздайте или выберите проект для продолжения", reply_markup=markup)
        return PROJECT


async def __create_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''создаем проект'''
    project_name = update.message.text

    
    user_data = context.user_data
    space_id = user_data['space_id']
    token = user_data['accessToken']
    key_project = str(user_data['key_project'])
    user_data['key_project'] = int(key_project) + 1

    err = action_project.create_project(TOKEN=token, space_id=space_id, project_name=project_name, key_project=key_project)

    markup = InlineKeyboardMarkup(keyboards.create_projects_keyboard(TOKEN=token, space_id=space_id))
    if err:
       await update.message.reply_text(
                            text="ОШИБКА \nСоздайте или выберите проект для продолжения", reply_markup=markup)
       return PROJECT
    else:
        await update.message.reply_text(
                            text="Проект созданно \nСоздайте или выберите проект для продолжения", reply_markup=markup)
        return PROJECT


#------------------board-------------------

async def __go_to_board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    token = user_data['accessToken']
    project_id = user_data['project_id']

    markup = InlineKeyboardMarkup(keyboards.create_boards_keyboard(token, project_id))

    await query.edit_message_text(
            text="Создайте или выберите доску", reply_markup=markup)
    
    return BOARD

async def __choice_board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''пользователь выбирает доску '''
    # получаем выбор пользователя
    query = update.callback_query
    await query.answer()
    index_board = int(query.data) - 2
    logger.info(index_board)

    #заносим выбор пользователя в context
    user_data = context.user_data
    token = user_data['accessToken']
    project_id = user_data['project_id']

    # получаем заносим выбранного пространства
    boards = action_board.get_boards(token, project_id)
    board_id = list(boards.keys())[index_board]
    user_data['board_id'] = board_id
    
    markup = InlineKeyboardMarkup(keyboards.board_menu_keyboard)

    await query.edit_message_text(
        text="Выберите действия c досками", reply_markup=markup
    )

    return ACTION_BOARD


async def __get_name_for_create_board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''получаем имя для доски'''
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Введите имя доски")
    return INPUT_NAME_FOR_BOARD


async def __delete_board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    
    token = user_data['accessToken']
    space_id = user_data['space_id']
    board_id = user_data['board_id']
    project_id = user_data['project_id']

    #удаляем доску
    err = action_board.delete_board(TOKEN=token, space_id=space_id, board_id=board_id)

    markup = InlineKeyboardMarkup(keyboards.create_boards_keyboard(TOKEN=token, project_id=project_id))

    if err:
       await query.edit_message_text(
                            text="ОШИБКА \nСоздайте или выберите доску для продолжения", reply_markup=markup)
       return BOARD
    else:
        await query.edit_message_text(
                            text="Доска удаленна \nСоздайте или выберите доску для продолжения", reply_markup=markup)
        return BOARD
    

async def __create_board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''создаем доску'''
    board_name = update.message.text

    
    user_data = context.user_data
    space_id = user_data['space_id']
    token = user_data['accessToken']
    project_id = user_data['project_id']

    err = action_board.create_board(TOKEN=token, space_id=space_id, board_name=board_name, project_id=project_id)

    markup = InlineKeyboardMarkup(keyboards.create_boards_keyboard(TOKEN=token, project_id=project_id))
    if err:
       await update.message.reply_text(
                            text="ОШИБКА \nСоздайте или выберите доску для продолжения", reply_markup=markup)
       return BOARD
    else:
        await update.message.reply_text(
                            text="Доска созданна \nСоздайте или выберите доску для продолжения", reply_markup=markup)
        return BOARD
    
#--------------colums--------------------------
async def __go_to_columns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    token = user_data['accessToken']
    board_id = user_data['board_id']

    markup = InlineKeyboardMarkup(keyboards.create_column_keyboard(token, board_id))

    await query.edit_message_text(
            text="Создайте или выберите колонку", reply_markup=markup)
    
    return COLUMN


async def __get_name_for_create_column(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''получаем имя для колонки'''
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Введите имя колонки")
    return INPUT_NAME_FOR_COLUMN


async def __choice_column(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''пользователь выбирает колонку '''
    # получаем выбор пользователя
    query = update.callback_query
    await query.answer()
    index_column = int(query.data) - 2
    logger.info(index_column)

    #заносим выбор пользователя в context
    user_data = context.user_data
    token = user_data['accessToken']
    board_id = user_data['board_id']

    # получаем заносим выбранного пространства
    columns = action_columns.get_columns(token, board_id)
    column_id = list(columns.keys())[index_column]
    user_data['column_id'] = column_id
    
    markup = InlineKeyboardMarkup(keyboards.column_menu_keyboard)

    await query.edit_message_text(
        text="Выберите действия c колонками", reply_markup=markup
    )

    return ACTION_COLUMN

async def __create_column(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''создаем колонку'''
    column_name = update.message.text

    
    user_data = context.user_data
    space_id = user_data['space_id']
    token = user_data['accessToken']
    project_id = user_data['project_id']
    board_id = user_data['board_id']

    err = action_columns.create_column(TOKEN=token,space_id=space_id,column_name=column_name, board_id=board_id, project_id=project_id)

    markup = InlineKeyboardMarkup(keyboards.create_column_keyboard(TOKEN=token, board_id=board_id))
    if err:
       await update.message.reply_text(
                            text="ОШИБКА \nСоздайте или выберите колонку для продолжения", reply_markup=markup)
       return COLUMN
    else:
        await update.message.reply_text(
                            text="Доска созданна \nСоздайте или выберите колонку для продолжения", reply_markup=markup)
        return COLUMN


async def __delete_column(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    
    token = user_data['accessToken']
    space_id = user_data['space_id']
    column_id = user_data['column_id']
    board_id = user_data['board_id']

    #удаляем колонку
    err = action_columns.delete_column(TOKEN=token, space_id=space_id, column_id=column_id)

    markup = InlineKeyboardMarkup(keyboards.create_column_keyboard(TOKEN=token, board_id=board_id))

    if err:
       await query.edit_message_text(
                            text="ОШИБКА \nСоздайте или выберите колонку для продолжения", reply_markup=markup)
       return COLUMN
    else:
        await query.edit_message_text(
                            text="Колонка удаленна \nСоздайте или выберите колонку для продолжения", reply_markup=markup)
        return COLUMN
    
#----------------tasks-----------------

async def __go_to_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    token = user_data['accessToken']
    column_id = user_data['column_id']

    markup = InlineKeyboardMarkup(keyboards.create_task_keyboard(token, column_id))

    await query.edit_message_text(
            text="Создайте или выберите задачу", reply_markup=markup)
    
    return TASK


async def __choice_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''пользователь выбирает задачу '''
    # получаем выбор пользователя
    query = update.callback_query
    await query.answer()
    index_task = int(query.data) - 2
    logger.info(index_task)

    #заносим выбор пользователя в context
    user_data = context.user_data
    token = user_data['accessToken']
    column_id = user_data['column_id']

    # получаем заносим выбранного пространства
    task = action_task.get_task(token, column_id)
    task_id = list(task.keys())[index_task]
    user_data['task_id'] = task_id
    
    markup = InlineKeyboardMarkup(keyboards.task_menu_keyboard)

    await query.edit_message_text(
        text="Выберите действия c задачами", reply_markup=markup
    )

    return ACTION_TASK


async def __delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    
    token = user_data['accessToken']
    space_id = user_data['space_id']
    task_id = user_data['task_id']
    column_id = user_data['column_id']

    #удаляем колонку
    err = action_task.delete_task(TOKEN=token, space_id=space_id, task_id=task_id)

    markup = InlineKeyboardMarkup(keyboards.create_task_keyboard(TOKEN=token, column_id=column_id))

    if err:
       await query.edit_message_text(
                            text="ОШИБКА \nСоздайте или выберите задачу для продолжения", reply_markup=markup)
       return TASK
    else:
        await query.edit_message_text(
                            text="Задача удаленна \nСоздайте или выберите задачу для продолжения", reply_markup=markup)
        return TASK
    

async def __get_name_for_create_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''получаем имя для задачи'''
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Введите название задачи")
    return INPUT_NAME_FOR_TASK


async def __create_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''создаем задачу'''
    task_name = update.message.text

    
    user_data = context.user_data
    space_id = user_data['space_id']
    token = user_data['accessToken']
    column_id = user_data['column_id']
    

    err = action_task.create_task(TOKEN=token,space_id=space_id,column_id=column_id, task_name=task_name)

    markup = InlineKeyboardMarkup(keyboards.create_task_keyboard(TOKEN=token, column_id=column_id))
    if err:
       await update.message.reply_text(
                            text="ОШИБКА \nСоздайте или выберите задачу для продолжения", reply_markup=markup)
       return TASK
    else:
        await update.message.reply_text(
                            text="Доска созданна \nСоздайте или выберите задачу для продолжения", reply_markup=markup)
        return TASK


def get_spaces() -> ConversationHandler:
    ONE, TWO, THREE, FOUR = range(4)


    spaces_handler= ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Мои пространства$'), __user_spaces),],
        states={
            #--------space----------
            SPACES: [
                CallbackQueryHandler(__get_name_for_create_spaces, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__choice_spaces)
            ],
            INPUT_NAME_FOR_SPACE:[
                MessageHandler(filters.TEXT, __create_space)
            ],
            ACTION_SPACE:[
                CallbackQueryHandler(__delete_spaces,  pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__go_to_project,  pattern="^" + str(TWO) + "$")
            ],

            #-------project---------
            PROJECT:[
                CallbackQueryHandler(__back_to_space, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__get_name_for_create_project, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(__choice_project)
            ],
            INPUT_NAME_FOR_PROJECT:[
                MessageHandler(filters.TEXT, __create_project)
            ],
            ACTION_PROJECT: [
                CallbackQueryHandler(__delete_project,  pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__go_to_board,  pattern="^" + str(TWO) + "$")
            ],

            #-------board----------
            BOARD:[
                CallbackQueryHandler(__go_to_project, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__get_name_for_create_board, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(__choice_board)
            ],
            INPUT_NAME_FOR_BOARD:[
                MessageHandler(filters.TEXT, __create_board)
            ],
            ACTION_BOARD: [
                CallbackQueryHandler(__delete_board,  pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__go_to_columns, pattern="^" + str(TWO) + "$")
            ],

            #-------colums---------
            COLUMN: [
                CallbackQueryHandler(__go_to_board, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__get_name_for_create_column, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(__choice_column)
            ],
            INPUT_NAME_FOR_COLUMN:[
                MessageHandler(filters.TEXT, __create_column)
            ],

            ACTION_COLUMN: [
                CallbackQueryHandler(__delete_column,  pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__go_to_task, pattern="^" + str(TWO) + "$")
            ],

            #-------tasks---------
            TASK:[
                CallbackQueryHandler(__go_to_columns, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__get_name_for_create_task, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(__choice_task)
            ],
            INPUT_NAME_FOR_TASK:[
                MessageHandler(filters.TEXT, __create_task)
            ],
            ACTION_TASK:[
                CallbackQueryHandler(__delete_task,  pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(__go_to_task, pattern="^" + str(TWO) + "$")
            ],

        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Назад в главное меню$"), __back_to_main_menu),
                   ],
    )

    return spaces_handler