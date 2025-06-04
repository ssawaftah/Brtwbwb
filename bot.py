import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ApplicationBuilder

TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: CallbackContext) -> None:
    buttons = [
        [InlineKeyboardButton("الدعم الفني", callback_data='support')],
        [InlineKeyboardButton("الأسعار", callback_data='pricing')],
        [InlineKeyboardButton("الموقع الرسمي", url='https://example.com')]
    ]
    
    await update.message.reply_text(
        "🔍 اختر أحد الخيارات:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'support':
        await query.edit_message_text("📩 تواصل مع الدعم: @SupportAccount")
    elif query.data == 'pricing':
        await query.edit_message_text("💲 باقات الخدمة:\n- الأساسية: 10$\n- المميزة: 20$")

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    application.run_polling()

if __name__ == '__main__':
    main()
