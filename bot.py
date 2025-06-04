import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = os.getenv('BOT_TOKEN')

def start(update: Update, context: CallbackContext) -> None:
    buttons = [
        [InlineKeyboardButton("الدعم الفني", callback_data='support')],
        [InlineKeyboardButton("الأسعار", callback_data='pricing')],
        [InlineKeyboardButton("الموقع الرسمي", url='https://example.com')]
    ]
    
    update.message.reply_text(
        "🔍 اختر أحد الخيارات:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'support':
        query.edit_message_text("📩 تواصل مع الدعم: @SupportAccount")
    elif query.data == 'pricing':
        query.edit_message_text("💲 باقات الخدمة:\n- الأساسية: 10$\n- المميزة: 20$")

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button_click))

updater.start_polling()
