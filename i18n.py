MESSAGES = {
    "ru": {
        "welcome": "👋 Привет! Отправь мне аудиофайл или ссылку для обработки.",
        "choose_lang": "🌐 Выберите язык:",
        "editing_tags": "🏷 **РЕДАКТИРОВАНИЕ ТЕГОВ**\n\n🎤 Исполнитель: **{artist}**\n🎵 Название: **{title}**\n💿 Альбом: **{album}**\n📅 Год: **{year}**",
        "btn_artist": "🎤 Исполнитель",
        "btn_title": "🎵 Название",
        "btn_album": "💿 Альбом",
        "btn_cover": "🖼 Обложка",
        "btn_main_menu": "🏠 Главное меню",
        "enter_artist": "Введите нового исполнителя:",
        "enter_title": "Введите новое название трека:",
        "enter_album": "Введите название альбома:",
        "enter_cover": "Отправьте изображение для обложки:"
    },
    "kk": {
        "welcome": "👋 Сәлем! Өңдеу үшін аудиофайл немесе сілтеме жіберіңіз.",
        "choose_lang": "🌐 Тілді таңдаңыз:",
        "editing_tags": "🏷 **ТЕГТЕРДІ ӨҢДЕУ**\n\n🎤 Орындаушы: **{artist}**\n🎵 Атауы: **{title}**\n💿 Альбом: **{album}**\n📅 Жыл: **{year}**",
        "btn_artist": "🎤 Орындаушы",
        "btn_title": "🎵 Атауы",
        "btn_album": "💿 Альбом",
        "btn_cover": "🖼 Мұқабаны ауыстыру",
        "btn_main_menu": "🏠 Басты мәзір",
        "enter_artist": "Жаңа орындаушыны енгізіңіз:",
        "enter_title": "Жаңа трек атауын енгізіңіз:",
        "enter_album": "Альбом атауын енгізіңіз:",
        "enter_cover": "Мұқаба үшін сурет жіберіңіз:"
    }
}

def get_msg(lang: str, key: str, **kwargs) -> str:
    lang_dict = MESSAGES.get(lang, MESSAGES["ru"])
    text = lang_dict.get(key, MESSAGES["ru"].get(key, ""))
    return text.format(**kwargs) if kwargs else text
