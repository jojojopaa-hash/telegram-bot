import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = "8744958495:AAHzpbL95CLHV4J377Js2o7FdRgItZOoRqY"
ADMIN_ID = 6014927893  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# храним связь сообщений
message_map = {}

WELCOME_TEXT = "Привет! Я Везунчик 👋\n\nЧем могу помочь?"

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Узнать о работе проводника", callback_data="work")],
        [InlineKeyboardButton("Чем занимается наш отряд", callback_data="life")],
        [InlineKeyboardButton("Как стать частью отряда", callback_data="join")],
        [InlineKeyboardButton("О курсах проводника", callback_data="courses")],
        [InlineKeyboardButton("Задать вопрос руководителю", callback_data="leader")],
        [InlineKeyboardButton("Анонимный чат", callback_data="anon")]
    ])

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад", callback_data="menu")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["anon"] = False
    await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu())

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu())

    elif query.data == "anon":
        context.user_data["anon"] = True
        await query.edit_message_text("✉️ Напиши сообщение", reply_markup=back_menu())

    else:
        context.user_data["anon"] = False
        await query.edit_message_text("Выбери пункт", reply_markup=back_menu())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # ======================
    # ЕСЛИ ПИШЕТ АДМИН (ОТВЕТ)
    # ======================
    if user.id == ADMIN_ID:
        if update.message.reply_to_message:
            original_msg_id = update.message.reply_to_message.message_id

            if original_msg_id in message_map:
                target_user_id = message_map[original_msg_id]

                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"📩 Ответ от куратора:\n\n{update.message.text}"
                )

                await update.message.reply_text("✅ Ответ отправлен")
                return

    # ======================
    # ЕСЛИ ПОЛЬЗОВАТЕЛЬ
    # ======================
    if context.user_data.get("anon"):
        sent = await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Новое сообщение\n\nID: {user.id}\n\n{update.message.text}"
        )

        # сохраняем связь
        message_map[sent.message_id] = user.id

        await update.message.reply_text("✅ Сообщение отправлено", reply_markup=main_menu())
        context.user_data["anon"] = False
        return

    await update.message.reply_text("Используй кнопки 👇", reply_markup=main_menu())

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот с чатом без /reply запущен...")
app.run_polling()
