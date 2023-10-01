from telegram import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)

from app.handlers.service.action_space import get_user_spaces
from app.handlers.service.action_project import get_projects
from app.handlers.service.action_board import get_boards
from app.handlers.service.action_columns import get_columns
from app.handlers.service.action_task import get_task

__stage = [i for i in range(4)]

spaces_menu_keyboard = [
        [InlineKeyboardButton('Удалить',callback_data=str(__stage[0]))],
        [InlineKeyboardButton('➡️Перейти в проект➡️', callback_data=str(__stage[1]))]
    ]

project_menu_keyboard = [
        [InlineKeyboardButton('Удалить',callback_data=str(__stage[0]))],
        [InlineKeyboardButton('➡️Перейти в доски➡️', callback_data=str(__stage[1]))]
    ]

board_menu_keyboard = [
        [InlineKeyboardButton('Удалить',callback_data=str(__stage[0]))],
        [InlineKeyboardButton('➡️Перейти в колонки➡️', callback_data=str(__stage[1]))]
    ]

column_menu_keyboard = [
        [InlineKeyboardButton('Удалить',callback_data=str(__stage[0]))],
        [InlineKeyboardButton('➡️Перейти в задачи➡️', callback_data=str(__stage[1]))]
    ]

task_menu_keyboard = [
        [InlineKeyboardButton('Удалить',callback_data=str(__stage[0]))],
        [InlineKeyboardButton('⬅️Назад к задачам⬅️',callback_data=str(__stage[1]))]
]


back_to_menu = ReplyKeyboardMarkup([['⬅️ Назад в главное меню⬅️']], resize_keyboard=True, one_time_keyboard=True)

    

def create_spaces_keyboard(TOKEN):
    spaces_keyboard = []
    spaces = get_user_spaces(TOKEN)
    names = spaces.values()

    spaces_keyboard.append([InlineKeyboardButton('🆕Создать пространство🆕', callback_data=str(0))])

    for i, title in enumerate(names):
        spaces_keyboard.append([InlineKeyboardButton(title, callback_data=str(i+1))])

    return spaces_keyboard
    

def create_projects_keyboard(TOKEN, space_id):
    project_keyboard = []
    projects = get_projects(TOKEN, space_id)
    names = projects.values()

    project_keyboard.append([InlineKeyboardButton('⬅️Назад в пространство⬅️', callback_data=str(0))])
    project_keyboard.append([InlineKeyboardButton('🆕Создать проект🆕', callback_data=str(1))])
    
    for i, title in enumerate(names):
        project_keyboard.append([InlineKeyboardButton(title, callback_data=str(i+2))])

    return project_keyboard


def create_boards_keyboard(TOKEN, project_id):
    boards_keyboard = []
    boards = get_boards(TOKEN, project_id)
    names = boards.values()

    boards_keyboard.append([InlineKeyboardButton('⬅️Назад в проект⬅️', callback_data=str(0))])
    boards_keyboard.append([InlineKeyboardButton('🆕Создать доску🆕', callback_data=str(1))])

    for i, title in enumerate(names):
        boards_keyboard.append([InlineKeyboardButton(title, callback_data=str(i+2))])

    return boards_keyboard

def create_column_keyboard(TOKEN, board_id):
    columns_keyboard = []
    columns = get_columns(TOKEN, board_id)
    names = columns.values()

    columns_keyboard.append([InlineKeyboardButton('⬅️Назад в доски⬅️', callback_data=str(0))])
    columns_keyboard.append([InlineKeyboardButton('🆕Создать колонку🆕', callback_data=str(1))])

    for i, title in enumerate(names):
        columns_keyboard.append([InlineKeyboardButton(title, callback_data=str(i+2))])

    return columns_keyboard

def create_task_keyboard(TOKEN, column_id):
    task_keyboard = []
    tasks = get_task(TOKEN, column_id)
    names = tasks.values()

    task_keyboard.append([InlineKeyboardButton('⬅️Назад в колонки⬅️', callback_data=str(0))])
    task_keyboard.append([InlineKeyboardButton('🆕Создать задачу🆕', callback_data=str(1))])

    for i, title in enumerate(names):
        task_keyboard.append([InlineKeyboardButton(title, callback_data=str(i+2))])

    return task_keyboard