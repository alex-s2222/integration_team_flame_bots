from telegram import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)

from app.handlers.service.action_space import get_user_spaces

__stage = [i for i in range(4)]

spaces_menu_keyboard = [
        [InlineKeyboardButton('Создать', callback_data=str(__stage[0]))],
        [InlineKeyboardButton('Удалить',callback_data=str(__stage[1]))],
        [InlineKeyboardButton('Перейти в проект', callback_data=str(__stage[2]))]
    ]

back_to_menu = ReplyKeyboardMarkup([['⬅️ Назад в главное меню']], resize_keyboard=True, one_time_keyboard=True)

    

def create_spaces_keyboard(TOKEN):
    spaces_keyboard = []
    spaces = get_user_spaces(TOKEN)
    names = spaces.values()

    spaces_keyboard.append([InlineKeyboardButton('Создать пространство', callback_data=str(0))])

    for i, title in enumerate(names):
        spaces_keyboard.append([InlineKeyboardButton(title, callback_data=str(i+1))])

    return spaces_keyboard
    
