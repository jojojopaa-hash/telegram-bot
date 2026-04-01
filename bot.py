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

# ==========================================
# НАСТРОЙКИ
# ==========================================

BOT_TOKEN = "8744958495:AAHzpbL95CLHV4J377Js2o7FdRgItZOoRqY"
ADMIN_ID = 1458837595  


# ==========================================
# ЛОГИ
# ==========================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ==========================================
# ТЕКСТЫ
# ==========================================

WELCOME_TEXT = (
    'Привет! Я Везунчик, главный помощник студенческого отряда проводников "Фортуна".\n\n'
    "Чем могу помочь?"
)

WORK_TEXT = (
    "Перед отправлением:\n"
    "🔻Подготовка вагона к рейсу (уборка, проверка оборудования, постельного белья)\n"
    "🔻Проверка билетов и документов пассажиров\n"
    "🔻Посадка пассажиров, помощь с багажом\n\n"
    "Во время поездки:\n"
    "🔸Обслуживание пассажиров (чай, постель, информация)\n"
    "🔸Контроль порядка и безопасности в вагоне\n"
    "🔸Проверка билетов при необходимости\n"
    "🔸Поддержание чистоты\n"
    "🔸Оказание первой помощи при необходимости\n\n"
    "По прибытии в город:\n"
    "🔹Высадка пассажиров\n"
    "🔹Проверка состояния вагона\n"
    "🔹Сдача отчёта и подготовка к следующему рейсу"
)

LIFE_TEXT = (
    "Мы не только выезжаем работать в летние и зимние каникулы, но и ведём активную "
    "социальную студенческую жизнь, а именно:\n\n"
    "💭Принимаем участие в вузовских, городских, республиканских и окружных мероприятиях "
    "(концерты, молодёжные слёты, образовательные форумы и многое другое). "
    "И всё это БЕСПЛАТНО\n"
    "💭Сами организовываем мероприятия разных уровней и получаем интересный опыт\n"
    "💭Реализуем свои таланты (спорт, искусство, танцы, вокал и многое другое)\n"
    "💭Находим верных друзей и полезные связи\n\n"
    "Одним словом, с нами никогда не будет скучно!🤘"
)

JOIN_TEXT = (
    "✅Тебе есть 18 лет\n"
    "✅Ты прошёл курсы проводника\n"
    "✅У тебя есть желание стать лучшей версией себя\n"
    "✅Хочешь раскрыть свой потенциал\n\n"
    "Тогда тебе к нам!\n\n"
    "P.s. Если ты ищешь только подработку на лето или зиму в качестве проводника, "
    "достаточно первых двух пунктов❗️"
)

COURSES_TEXT = (
    "Чтобы стать проводником пассажирского вагона тебе нужно пройти курсы проводника. "
    "Вот всё, что тебе нужно о них знать:\n\n"
    "🔹Стоимость обучения 2090 рублей\n"
    "🔹Есть возможность обучаться заочно на платформе Академия РСО\n"
    "🔹Длительность зависит только от тебя. Обучаешься как и когда тебе удобно\n"
    "🔹Куратор с тобой на связи 24/7\n"
    "🔹Ты получишь сертификат проводника и новая профессия у тебя в кармане"
)

LEADER_TEXT = (
    "Если у тебя остались вопросы, то смело пиши командиру отряда Руслане:\n"
    "👉 https://t.me/bby_xannnny"
)

ANON_CHAT_TEXT = (
    "✉️ Напиши своё сообщение.\n\n"
    "Оно будет отправлено куратору."
)


# ==========================================
# КЛАВИАТУРЫ
# ==========================================

def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Узнать о работе проводника", callback_data="work")],
        [InlineKeyboardButton("Чем занимается наш отряд, кроме работы", callback_data="life")],
        [InlineKeyboardButton("Как стать частью нашего отряда", callback_data="join")],
        [InlineKeyboardButton("О курсах проводника", callback_data="courses")],
        [InlineKeyboardButton("Задать вопрос руководителю отряда", callback_data="leader")],
        [InlineKeyboardButton("Анонимный чат", callback_data="anon_chat")],
    ])


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад в меню", callback_data="menu")]
    ])


# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================

async def send_main_menu(chat) -> None:
    await chat.send_message(
        WELCOME_TEXT,
        reply_markup=main_menu_keyboard(),
        disable_web_page_preview=True,
    )


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# ==========================================
# КОМАНДЫ
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["waiting_for_anon_message"] = False
    if update.effective_chat:
        await send_main_menu(update.effective_chat)


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["waiting_for_anon_message"] = False
    if update.effective_chat:
        await send_main_menu(update.effective_chat)


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["waiting_for_anon_message"] = False
    if update.effective_message:
        await update.effective_message.reply_text(
            "Действие отменено.",
            reply_markup=main_menu_keyboard(),
        )


async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user and update.effective_message:
        await update.effective_message.reply_text(
            f"Твой Telegram ID: {update.effective_user.id}"
        )


async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_message:
        return

    if not is_admin(update.effective_user.id):
        await update.effective_message.reply_text("У тебя нет доступа к этой команде.")
        return

    if len(context.args) < 2:
        await update.effective_message.reply_text(
            "Неправильный формат.\n\n"
            "Пример:\n"
            "/reply 123456789 Привет, отвечаю на твой вопрос"
        )
        return

    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.effective_message.reply_text(
            "Первый аргумент должен быть числом.\n\n"
            "Пример:\n"
            "/reply 123456789 Привет, отвечаю на твой вопрос"
        )
        return

    reply_text = " ".join(context.args[1:]).strip()

    if not reply_text:
        await update.effective_message.reply_text("Текст ответа пустой.")
        return

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"📩 Ответ от куратора:\n\n{reply_text}",
        )
        await update.effective_message.reply_text("✅ Ответ отправлен.")
    except Exception as e:
        logger.exception("Ошибка отправки ответа пользователю: %s", e)
        await update.effective_message.reply_text(
            "❌ Не удалось отправить ответ.\n"
            "Возможно, пользователь ещё не нажал /start у бота."
        )


# ==========================================
# КНОПКИ
# ==========================================

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    if query.data == "menu":
        context.user_data["waiting_for_anon_message"] = False
        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=main_menu_keyboard(),
            disable_web_page_preview=True,
        )
        return

    if query.data == "work":
        context.user_data["waiting_for_anon_message"] = False
        await query.edit_message_text(
            WORK_TEXT,
            reply_markup=back_keyboard(),
            disable_web_page_preview=True,
        )
        return

    if query.data == "life":
        context.user_data["waiting_for_anon_message"] = False
        await query.edit_message_text(
            LIFE_TEXT,
            reply_markup=back_keyboard(),
            disable_web_page_preview=True,
        )
        return

    if query.data == "join":
        context.user_data["waiting_for_anon_message"] = False
        await query.edit_message_text(
            JOIN_TEXT,
            reply_markup=back_keyboard(),
            disable_web_page_preview=True,
        )
        return

    if query.data == "courses":
        context.user_data["waiting_for_anon_message"] = False
        await query.edit_message_text(
            COURSES_TEXT,
            reply_markup=back_keyboard(),
            disable_web_page_preview=True,
        )
        return

    if query.data == "leader":
        context.user_data["waiting_for_anon_message"] = False
        await query.edit_message_text(
            LEADER_TEXT,
            reply_markup=back_keyboard(),
            disable_web_page_preview=False,
        )
        return

    if query.data == "anon_chat":
        context.user_data["waiting_for_anon_message"] = True
        await query.edit_message_text(
            ANON_CHAT_TEXT,
            reply_markup=back_keyboard(),
            disable_web_page_preview=True,
        )
        return


# ==========================================
# ОБРАБОТКА ТЕКСТА
# ==========================================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message or not update.effective_user:
        return

    text = update.effective_message.text
    waiting_for_anon = context.user_data.get("waiting_for_anon_message", False)

    if waiting_for_anon:
        user = update.effective_user
        full_name = user.full_name
        username = f"@{user.username}" if user.username else "нет username"
        user_id = user.id

        admin_message = (
            "📩 Новое сообщение из анонимного чата\n\n"
            f"Отправитель: {full_name}\n"
            f"Username: {username}\n"
            f"User ID: {user_id}\n\n"
            f"Сообщение:\n{text}\n\n"
            f"Чтобы ответить, используй команду:\n"
            f"/reply {user_id} ТВОЙ_ОТВЕТ"
        )

        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=admin_message,
                disable_web_page_preview=True,
            )
            await update.effective_message.reply_text(
                "✅ Сообщение отправлено.",
                reply_markup=main_menu_keyboard(),
            )
        except Exception as e:
            logger.exception("Ошибка отправки админу: %s", e)
            await update.effective_message.reply_text(
                "❌ Не удалось отправить сообщение. Попробуй позже.",
                reply_markup=main_menu_keyboard(),
            )

        context.user_data["waiting_for_anon_message"] = False
        return

    await update.effective_message.reply_text(
        "Используй кнопки меню ниже или команды /start и /menu.",
        reply_markup=main_menu_keyboard(),
    )


# ==========================================
# ОШИБКИ
# ==========================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Ошибка в боте:", exc_info=context.error)


# ==========================================
# ЗАПУСК
# ==========================================

def main() -> None:
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .connect_timeout(20.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .pool_timeout(30.0)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_error_handler(error_handler)

    print("Бот запущен...")
    app.run_polling(
        drop_pending_updates=True,
        poll_interval=1.5,
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    main()
