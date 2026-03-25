import asyncio
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = "8744958495:AAHzpbL95CLHV4J377Js2o7FdRgItZOoRqY"

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("fortuna_bot")

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
    "(концерты, молодёжные слёты, образовательные форумы и многое другое). И всё это БЕСПЛАТНО\n"
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
    "Тогда тебе к нам!\n"
    "P.s. Если ты ищешь только подработку на лето или зиму в качестве проводника, "
    "достаточно первых двух пунктов❗️"
)

COURSES_TEXT = (
    "Чтобы стать проводником пассажирского вагона тебе нужно пройти курсы проводника. "
    "Вот всё, что тебе нужно о них знать:\n"
    "🔹Стоимость обучения 2090 рублей\n"
    "🔹Есть возможность обучаться заочно на платформе Академия РСО\n"
    "🔹Длительность зависит только от тебя. Обучаешься как и когда тебе удобно\n"
    "🔹Куратор с тобой на связи 24/7\n"
    "🔹Ты получишь сертификат проводника и новая профессия у тебя в кармане"
)

LEADER_TEXT = (
    "Если у тебя остались вопросы, то смело пиши командиру отряда Руслане\n"
    "https://t.me/bby_xannnny"
)


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Узнать о работе проводника", callback_data="work")],
        [InlineKeyboardButton("Чем занимается наш отряд, кроме работы", callback_data="life")],
        [InlineKeyboardButton("Как стать частью нашего отряда", callback_data="join")],
        [InlineKeyboardButton("О курсах проводника", callback_data="courses")],
        [InlineKeyboardButton("Задать вопрос руководителю отряда", callback_data="leader")],
    ])


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад в меню", callback_data="menu")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            WELCOME_TEXT,
            reply_markup=main_menu_keyboard(),
            disable_web_page_preview=True,
        )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            WELCOME_TEXT,
            reply_markup=main_menu_keyboard(),
            disable_web_page_preview=True,
        )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    if query.data == "menu":
        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=main_menu_keyboard(),
            disable_web_page_preview=True,
        )
        return

    if query.data == "work":
        text = WORK_TEXT
    elif query.data == "life":
        text = LIFE_TEXT
    elif query.data == "join":
        text = JOIN_TEXT
    elif query.data == "courses":
        text = COURSES_TEXT
    elif query.data == "leader":
        text = LEADER_TEXT
    else:
        text = "Неизвестная команда. Нажми /start"

    await query.edit_message_text(
        text,
        reply_markup=back_keyboard(),
        disable_web_page_preview=False,
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Ошибка в боте", exc_info=context.error)


def build_app():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(60.0)
        .write_timeout(60.0)
        .pool_timeout(30.0)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_error_handler(error_handler)

    return app


async def run_bot_forever():
    while True:
        try:
            logger.info("Пробую запустить бота...")
            app = build_app()

            await app.initialize()
            await app.start()
            await app.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES,
                poll_interval=2.0,
            )

            logger.info("Бот успешно запущен.")

            while True:
                await asyncio.sleep(60)

        except Exception as e:
            logger.exception("Бот не смог подключиться или упал: %s", e)
            logger.info("Повторная попытка через 15 секунд...")
            await asyncio.sleep(15)
        finally:
            try:
                await app.updater.stop()
            except Exception:
                pass
            try:
                await app.stop()
            except Exception:
                pass
            try:
                await app.shutdown()
            except Exception:
                pass


if __name__ == "__main__":
    asyncio.run(run_bot_forever())