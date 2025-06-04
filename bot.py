import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
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

async def start(update: Update, context: CallbackContext, from_button: bool = False) -> None:
    user = update.effective_user
    welcome_message = (
        f"مرحبًا {user.first_name} في بوت قصص أحمد،\n"
        "استمتع/ي بقراءة القصص في سرية تامة على @Sexz91bot.\n\n"
        "📚 القصص الشائعة هذا الأسبوع:"
    )
    
    # أزرار القصص الشائعة
    stories_buttons = [
        [InlineKeyboardButton("القصة 1: رحلة الغموض", callback_data='story_1')],
        [InlineKeyboardButton("القصة 2: الحب السري", callback_data='story_2')],
        [InlineKeyboardButton("القصة 3: الليلة الموعودة", callback_data='story_3')],
        [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data='main_menu')]
    ]
    
    # أزرار الأقسام مع زر الرئيسية
    categories_buttons = [
        ["قصص سكس"],
        ["قصص سكس محارم"],
        ["قصص سكس سحاق"],
        ["قصص سكس دياثة"],
        ["🏠 القائمة الرئيسية"]
    ]
    
    if from_button:
        await update.callback_query.edit_message_text(
            text=welcome_message,
            reply_markup=InlineKeyboardMarkup(stories_buttons)
        )
    else:
        await update.message.reply_text(
            text=welcome_message,
            reply_markup=InlineKeyboardMarkup(stories_buttons)
        )
        
        await update.message.reply_text(
            text="أو يمكنك تصفح القصص حسب الأقسام:",
            reply_markup=ReplyKeyboardMarkup(
                categories_buttons,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

async def handle_stories(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'main_menu':
        await start(update, context, from_button=True)
        return
    
    story_data = query.data
    stories = {
        'story_1': {
            'title': "رحلة الغموض",
            'content': "هنا محتوى القصة الأولى...\n\nرابط القراءة: @Sexz91bot/story1",
            'buttons': [
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data='main_menu')]
            ]
        },
        'story_2': {
            'title': "الحب السري",
            'content': "هنا محتوى القصة الثانية...\n\nرابط القراءة: @Sexz91bot/story2",
            'buttons': [
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data='main_menu')]
            ]
        },
        'story_3': {
            'title': "الليلة الموعودة",
            'content': "هنا محتوى القصة الثالثة...\n\nرابط القراءة: @Sexz91bot/story3",
            'buttons': [
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data='main_menu')]
            ]
        }
    }
    
    if story_data in stories:
        story = stories[story_data]
        await query.edit_message_text(
            text=f"📖 {story['title']}\n\n{story['content']}",
            reply_markup=InlineKeyboardMarkup(story['buttons'])
        )

async def handle_categories(update: Update, context: CallbackContext) -> None:
    if update.message.text == "🏠 القائمة الرئيسية":
        await start(update, context)
        return
    
    category = update.message.text
    categories = {
        "قصص سكس": {
            "name": "قصص سكس",
            "buttons": [
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data='main_menu')]
            ]
        },
        "قصص سكس محارم": {
            "name": "قصص سكس محارم",
            "buttons": [
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data='main_menu')]
            ]
        },
        "قصص سكس سحاق": {
            "name": "قصص سكس سحاق",
            "buttons": [
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data='main_menu')]
            ]
        },
        "قصص سكس الدياثة": {
            "name": "قصص سكس الدياثة",
            "buttons": [
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data='main_menu')]
            ]
        }
    }
    
    if category in categories:
        cat_info = categories[category]
        await update.message.reply_text(
            text=f"تم اختيار قسم {cat_info['name']}\n"
                 "سيتم إرسال أفضل القصص في هذا القسم...\n\n"
                 "تابعنا على @Sexz91bot للحصول على المزيد",
            reply_markup=InlineKeyboardMarkup(cat_info['buttons'])
        )

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_stories))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_categories))
    
    application.run_polling()

if __name__ == '__main__':
    main()

