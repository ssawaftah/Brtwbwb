import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    filters
)

TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_message = (
        f"مرحبًا {user.first_name} في بوت قصص أحمد،\n"
        "استمتع/ي بقراءة القصص في سرية تامة على @Sexz91bot.\n\n"
        "📚 القصص الشائعة هذا الأسبوع:"
    )
    
    # أزرار القصص الشائعة (Inline Keyboard)
    stories_buttons = [
        [InlineKeyboardButton("القصة 1: رحلة الغموض", callback_data='story_1')],
        [InlineKeyboardButton("القصة 2: الحب السري", callback_data='story_2')],
        [InlineKeyboardButton("القصة 3: الليلة الموعودة", callback_data='story_3')]
    ]
    
    # أزرار الأقسام (Reply Keyboard)
    categories_buttons = [
        ["🔞 قسم القصص الجريئة", "📖 قسم القصص الرومانسية"],
        ["🕵️ قسم القصص الغامضة", "🎭 قسم القصص الدرامية"]
    ]
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=InlineKeyboardMarkup(stories_buttons)
    
    await update.message.reply_text(
        "أو يمكنك تصفح القصص حسب الأقسام:",
        reply_markup=ReplyKeyboardMarkup(
            categories_buttons,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

async def handle_stories(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    story_data = query.data
    stories = {
        'story_1': {
            'title': "رحلة الغموض",
            'content': "هنا محتوى القصة الأولى...\n\nرابط القراءة: @Sexz91bot/story1"
        },
        'story_2': {
            'title': "الحب السري",
            'content': "هنا محتوى القصة الثانية...\n\nرابط القراءة: @Sexz91bot/story2"
        },
        'story_3': {
            'title': "الليلة الموعودة",
            'content': "هنا محتوى القصة الثالثة...\n\nرابط القراءة: @Sexz91bot/story3"
        }
    }
    
    if story_data in stories:
        story = stories[story_data]
        await query.edit_message_text(
            f"📖 {story['title']}\n\n{story['content']}"
        )

async def handle_categories(update: Update, context: CallbackContext) -> None:
    category = update.message.text
    categories = {
        "🔞 قسم القصص الجريئة": "جريئة",
        "📖 قسم القصص الرومانسية": "رومانسية",
        "🕵️ قسم القصص الغامضة": "غامضة",
        "🎭 قسم القصص الدرامية": "درامية"
    }
    
    if category in categories:
        await update.message.reply_text(
            f"تم اختيار قسم {categories[category]}\n"
            "سيتم إرسال أفضل القصص في هذا القسم...\n\n"
            "تابعنا على @Sexz91bot للحصول على المزيد"
        )

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    
    # handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_stories))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_categories))
    
    application.run_polling()

if __name__ == '__main__':
    main()
