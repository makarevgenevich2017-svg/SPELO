import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

# === КОНФИГУРАЦИЯ ===
BOT_TOKEN = "9129504889:AAGmB3POF60jom0AGCcHMlzspcfHWw80ej8"
ADMIN_ID = 5190022426
WEBAPP_URL = "https://makarevgenevich2017-svg.github.io/SPELO/SPELO_F1.html"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    # Клавиатура с кнопкой WebApp (обязательно для работы sendData!)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🧺 Собрать бокс СПЕЛО",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ],
        resize_keyboard=True,
    )

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в сервис свежих фермерских продуктов **СПЕЛО**.\n"
        "Нажми кнопку ниже, чтобы открыть конструктор бокса и оформить заказ.",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    try:
        raw_data = message.web_app_data.data
        order = json.loads(raw_data)
    except Exception as e:
        logging.error(f"Ошибка парсинга данных: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке данных заказа.")
        return

    user = message.from_user
    tg_user = f"@{user.username}" if user.username else f"ID: {user.id}"

    # Красивая карточка для тебя (админа)
    admin_card = (
        f"🚨 <b>НОВЫЙ ЗАКАЗ В СПЕЛО ({order.get('order_id', 'б/н')})</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📦 <b>Бокс:</b> {order.get('box_type')} (Размер {order.get('box_size')})\n"
        f"💰 <b>Сумма к оплате:</b> {order.get('price')} ₽\n"
        f"🚫 <b>Стоп-лист:</b> {order.get('stop_list')}\n\n"
        f"👤 <b>Получатель:</b> {order.get('client_name')}\n"
        f"📱 <b>Телефон:</b> {order.get('phone')}\n"
        f"✉️ <b>Почта:</b> {order.get('email')}\n"
        f"✈️ <b>Telegram профиль:</b> {tg_user}\n\n"
        f"📍 <b>Адрес/Самовывоз:</b> {order.get('address')}\n"
        f"📅 <b>Дата доставки:</b> {order.get('delivery_date')}\n"
        f"🚪 <b>Безопасное место:</b> {order.get('safe_place')}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    # 1. Отправляем уведомление админу
    await bot.send_message(chat_id=ADMIN_ID, text=admin_card, parse_mode="HTML")

    # 2. Отправляем подтверждение пользователю в чат
    user_confirm = (
        f"✅ <b>Заказ {order.get('order_id')} успешно оформлен!</b>\n\n"
        f"Вы выбрали: <b>{order.get('box_type')} ({order.get('box_size')})</b> на сумму <b>{order.get('price')} ₽</b>.\n"
        f"Дата доставки: {order.get('delivery_date')}.\n\n"
        "Мы уже получили вашу заявку и начали комплектацию. Спасибо, что вы со СПЕЛО! 🍏"
    )
    await message.answer(user_confirm, parse_mode="HTML")


async def main():
    print("Бот СПЕЛО успешно запущен и слушает события...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())