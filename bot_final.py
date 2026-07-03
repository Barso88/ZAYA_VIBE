import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8875465912:AAFlkBVyqFUyM5sdZhenL6h3M20yCrh9G-I"
CHANNEL_ID = "@zaya_vaibkodim"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        
        if member.status in ["creator", "administrator", "member"]:
            await send_prompt(update, context, user_name)
        else:
            await ask_to_subscribe(update)
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await ask_to_subscribe(update)

async def treker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /трекер - отправляет гайд по трекеру воды"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        
        if member.status in ["creator", "administrator", "member"]:
            await update.message.reply_text(
                f"Привет, {user_name}! 💜\n\n"
                "Вот гайд по созданию трекера воды 👇"
            )
            
            try:
                with open('vibecoding_water_tracker_guide.pdf', 'rb') as pdf_file:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=pdf_file,
                        caption="Вайбкодинг: трекер воды 🌸\nПолный гайд для создания на телефоне"
                    )
                
                await update.message.reply_text("Создавай и делись результатом! 💪")
                
            except FileNotFoundError:
                await update.message.reply_text(
                    "Ошибка: файл гайда не найден."
                )
        else:
            await ask_to_subscribe(update)
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await ask_to_subscribe(update)

async def ask_to_subscribe(update: Update) -> None:
    keyboard = [
        [InlineKeyboardButton("✅ Подписаться на канал", url="https://t.me/zaya_vaibkodim")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Привет, зая! 💜\n\n"
        "Чтобы получить контент вайбкодинга, подпишись на канал 👇\n\n"
        "После подписки введи команду и получишь всё! 🚀",
        reply_markup=reply_markup
    )

async def send_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, user_name: str) -> None:
    await update.message.reply_text(
        f"Спасибо что подписалась, {user_name}! 💜\n\n"
        "Вот твой волшебный промпт для вайбкодинга 👇"
    )
    
    try:
        with open('vibecoding_prompt.pdf', 'rb') as pdf_file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=pdf_file,
                caption="Вайбкодинг промпт - сохрани себе 📄"
            )
        
        await update.message.reply_text(
            "Попробуй эти команды:\n"
            "/трекер - гайд по трекеру воды 🌸\n\n"
            "Не поняла что-то? Пиши в комментах! 💪"
        )
        
    except FileNotFoundError:
        await update.message.reply_text(
            "Ошибка: файл промпта не найден в папке."
        )
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка при отправке. Попробуй позже!")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("трекер", treker))  # ← НОВАЯ КОМАНДА
    
    print("✅ Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()