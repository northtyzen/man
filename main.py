import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from session_manager import session_mgr
from i18n import get_msg

BOT_TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_ЕСЛИ_НЕТ_ENV")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# --- Клавиатуры ---
def get_lang_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru"),
            InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="set_lang_kk")
        ]
    ])

def get_main_menu_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏷 " + ("Теги" if lang == "ru" else "Тегтер"), callback_data="edit_tags")],
        [InlineKeyboardButton(text="🌐 " + ("Язык" if lang == "ru" else "Тіл"), callback_data="change_lang")]
    ])

def get_tags_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_msg(lang, "btn_artist"), callback_data="tag_artist"),
            InlineKeyboardButton(text=get_msg(lang, "btn_title"), callback_data="tag_title")
        ],
        [
            InlineKeyboardButton(text=get_msg(lang, "btn_album"), callback_data="tag_album"),
            InlineKeyboardButton(text=get_msg(lang, "btn_cover"), callback_data="tag_cover")
        ],
        [
            InlineKeyboardButton(text=get_msg(lang, "btn_main_menu"), callback_data="back_to_menu")
        ]
    ])

# --- Хэндлеры ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    session = session_mgr.get_session(message.from_user.id)
    lang = session["lang"]
    await message.answer(get_msg(lang, "welcome"), reply_markup=get_lang_kb())

@dp.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[2]
    session_mgr.update_session(callback.from_user.id, lang=lang)
    await callback.message.edit_text(
        get_msg(lang, "welcome"),
        reply_markup=get_main_menu_kb(lang)
    )
    await callback.answer()

@dp.callback_query(F.data == "change_lang")
async def change_lang(callback: types.CallbackQuery):
    session = session_mgr.get_session(callback.from_user.id)
    await callback.message.edit_text(
        get_msg(session["lang"], "choose_lang"),
        reply_markup=get_lang_kb()
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    session = session_mgr.get_session(callback.from_user.id)
    lang = session["lang"]
    await callback.message.edit_text(
        get_msg(lang, "welcome"),
        reply_markup=get_main_menu_kb(lang)
    )
    await callback.answer()

# Прием аудиофайла
@dp.message(F.audio)
async def handle_audio(message: types.Message):
    audio = message.audio
    user_id = message.from_user.id
    
    session_mgr.update_session(
        user_id,
        file_id=audio.file_id,
        title=audio.title or "Unknown",
        artist=audio.performer or "Unknown"
    )
    session = session_mgr.get_session(user_id)
    lang = session["lang"]

    text = get_msg(
        lang, "editing_tags",
        artist=session["artist"],
        title=session["title"],
        album=session["album"],
        year=session["year"]
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=get_tags_kb(lang))

@dp.callback_query(F.data == "edit_tags")
async def edit_tags_menu(callback: types.CallbackQuery):
    session = session_mgr.get_session(callback.from_user.id)
    lang = session["lang"]
    text = get_msg(
        lang, "editing_tags",
        artist=session["artist"],
        title=session["title"],
        album=session["album"],
        year=session["year"]
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_tags_kb(lang))
    await callback.answer()

@dp.callback_query(F.data.startswith("tag_"))
async def prompt_tag_change(callback: types.CallbackQuery):
    tag_type = callback.data.split("_")[1]
    user_id = callback.from_user.id
    session = session_mgr.get_session(user_id)
    lang = session["lang"]

    session_mgr.update_session(user_id, state=f"waiting_{tag_type}")

    prompt_key = f"enter_{tag_type}"
    prompt_text = get_msg(lang, prompt_key)
    await callback.message.answer(prompt_text)
    await callback.answer()

@dp.message(F.text & ~F.text.startswith("/"))
async def process_text_input(message: types.Message):
    user_id = message.from_user.id
    session = session_mgr.get_session(user_id)
    state = session.get("state")

    if not state:
        return

    lang = session["lang"]
    if state == "waiting_artist":
        session_mgr.update_session(user_id, artist=message.text, state=None)
    elif state == "waiting_title":
        session_mgr.update_session(user_id, title=message.text, state=None)
    elif state == "waiting_album":
        session_mgr.update_session(user_id, album=message.text, state=None)

    session = session_mgr.get_session(user_id)
    text = get_msg(
        lang, "editing_tags",
        artist=session["artist"],
        title=session["title"],
        album=session["album"],
        year=session["year"]
    )
    await message.answer("✅ Данные обновлены!\n\n" + text, parse_mode="Markdown", reply_markup=get_tags_kb(lang))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

