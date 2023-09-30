from telegram import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)


__stage = [i for i in range(4)]

spaces_menu_keyboard = [
        [InlineKeyboardButton('Создать', callback_data=str(__stage[0]))],
        [InlineKeyboardButton('Удалить',callback_data=str(__stage[1]))],
        [InlineKeyboardButton('Редактировать', callback_data=str(__stage[2]))],
        [InlineKeyboardButton('Выбор для перехода в проект', callback_data=str(__stage[3]))]
    ]
    