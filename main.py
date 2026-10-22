import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from google import genai

# Loggingni yoqish
logging.basicConfig(level=logging.INFO)

# Token va API kalitlarni muhit o'zgaruvchilaridan (Environment variables) olish
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# Bot va Dispatcher obyektlarini yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Gemini AI mijozini sozlash
ai_client = genai.Client(api_key=GEMINI_API_KEY)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """/start buyrug'iga javob berish"""
    text = (
        f"Salom, {message.from_user.full_name}! 👋\n\n"
        "Men Sun'iy Intellekt (AI) botiman. Menga istalgan savolingizni "
        "yuborishingiz mumkin, bajonidil javob beraman!"
    )
    await message.answer(text)


@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    """Muloqotni tozalash buyrug'i"""
    await message.answer("Suhbat tarixi tozalandi. Yangi savolingizni bering!")


@dp.message(F.text)
async def handle_ai_response(message: types.Message):
    """Foydalanuvchi matn yuborganda AI orqali javob qaytarish"""
    # Foydalanuvchiga bot o'ylayotganini ko'rsatish ("typing..." statusi)
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        # Gemini AI modelidan javob olish
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
        )

        # AI javobini foydalanuvchiga yuborish
        await message.reply(response.text)

    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await message.reply("Kechirasiz, javob tayyorlashda xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring.")


async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())