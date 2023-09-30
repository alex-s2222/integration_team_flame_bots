from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from telegram import (
    Update,
)

from app.SETTINGS import TOKEN
from app.handlers.auth_service.auth.main import start
from app.handlers.auth_service.auth.sign_up import sign_up
from app.handlers.auth_service.auth.sign_in import sign_in

def run():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))

    # auth user
    app.add_handler(sign_up())
    app.add_handler(sign_in())

    #
    

    app.run_polling()
