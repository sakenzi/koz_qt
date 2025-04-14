from aiogram import Dispatcher, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters.command import Command
from dotenv import load_dotenv
import os
import asyncio
from api_handlers.exe_file_api import fetch_exe_files
from controllers.exe_file_controller import download_and_save_files


all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
os.makedirs(all_media_dir, exist_ok=True)

load_dotenv()

token_bot = os.getenv("TOKEN")

bot = Bot(token=token_bot)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    username = message.from_user.username
    await message.answer(f"Сәлем {username}!\n Қосымшаны алу үшін, /exe командасын басыңыз және күтіңіз.\n\n"
                          f"Привет {username}!\n Щелкните команду /exe, чтобы получить приложение и ждите.")

@dp.message(Command("exe"))
async def cmd_exe(message: Message):
    files_data = await fetch_exe_files()
    if not files_data:
        await message.answer("Қазір қолжетімді файлдар жоқ.")
        return
    downloaded_files = await download_and_save_files(files_data, all_media_dir)
    if not downloaded_files:
        await message.answer("Ешқандай .exe файл жүктелмеді.")
        return
    for file_path in downloaded_files:
        file = FSInputFile(file_path)
        await message.answer_document(file)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())