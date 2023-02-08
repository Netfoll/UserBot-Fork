# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

import logging

from telethon.tl.types import Message

from .. import loader, translations, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
}


@loader.tds
class Translations(loader.Module):
    """Processes internal translations"""

    strings = {
        "name": "Translations",
        "lang_saved": "{} <b>Language saved!</b>",
        "pack_saved": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Translate pack"
            " saved!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Incorrect language"
            " specified</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Translations reset"
            " to default ones</b>"
        ),
        "check_pack": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Invalid pack format"
            " in url</b>"
        ),
        "check_url": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>You need to specify"
            " valid url containing a langpack</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>📁</emoji> <b>Command output seems"
            " to be too long, so it's sent in file.</b>"
        ),
        "opening_form": " <b>Opening form...</b>",
        "opening_gallery": " <b>Opening gallery...</b>",
        "opening_list": " <b>Opening list...</b>",
        "inline403": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>You can't send inline"
            " units in this chat</b>"
        ),
        "invoke_failed": "<b>🚫 Unit invoke failed! More info in logs</b>",
        "show_inline_cmds": "📄 Show all available inline commands",
        "no_inline_cmds": "You have no available commands",
        "no_inline_cmds_msg": (
            "<b>😔 There are no available inline commands or you lack access to them</b>"
        ),
        "inline_cmds": "ℹ️ You have {} available command(-s)",
        "inline_cmds_msg": "<b>ℹ️ Available inline commands:</b>\n\n{}",
        "run_command": "🏌️ Run command",
        "command_msg": "<b>🌘 Command «{}»</b>\n\n<i>{}</i>",
        "command": "🌘 Command «{}»",
        "button403": "You are not allowed to press this button!",
        "keep_id": "⚠️ Do not remove ID! {}",
        "choose_language": "🗽 <b>Choose language</b>",
        "not_official": (
            "<emoji document_id=5312383351217201533>⚠️</emoji> <b>This language is not"
            " officially supported</b>"
        ),
        "requested_join": (
            "💫 <b>Module</b> <code>{}</code> <b>requested to join channel <a"
            " href='https://t.me/{}'>{}</a></b>\n\n<b>❓ Reason:</b> <i>{}</i>"
        ),
        "fw_error": (
            "<emoji document_id=5877458226823302157>🕒</emoji> <b>Call"
            "</b> <code>{}</code> <b>caused FloodWait of {} on method"
            "</b> <code>{}</code>"
        ),
        "rpc_error": (
            "<emoji document_id=5877477244938489129>🚫</emoji> <b>Call"
            "</b> <code>{}</code> <b>failed due to RPC error:</b>"
            " <code>{}</code>"
        ),
    }

    strings_ru = {
        "lang_saved": "{} <b>Язык сохранён!</b>",
        "pack_saved": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Пакет переводов"
            " сохранён!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Указан неверный"
            " язык</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Переводы сброшены"
            " на стандартные</b>"
        ),
        "check_pack": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Неверный формат"
            " пакета переводов в ссылке</b>"
        ),
        "check_url": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Вы должны указать"
            " ссылку, содержащую пакет переводов</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>📁</emoji> <b>Вывод команды слишком"
            " длинный, поэтому он отправлен в файле.</b>"
        ),
        "opening_form": " <b>Открываю форму...</b>",
        "opening_gallery": " <b>Открываю галерею...</b>",
        "opening_list": " <b>Открываю список...</b>",
        "inline403": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Вы не можете"
            " отправлять встроенные элементы в этом чате</b>"
        ),
        "invoke_failed": "<b>🚫 Вызов модуля не удался! Подробнее в логах</b>",
        "show_inline_cmds": "📄 Показать все доступные встроенные команды",
        "no_inline_cmds": "У вас нет доступных inline команд",
        "no_inline_cmds_msg": (
            "<b>😔 Нет доступных inline команд или у вас нет доступа к ним</b>"
        ),
        "inline_cmds": "ℹ️ У вас {} доступная(-ых) команда(-ы)",
        "inline_cmds_msg": "<b>ℹ️ Доступные inline команды:</b>\n\n{}",
        "run_command": "🏌️ Выполнить команду",
        "command_msg": "<b>🌘 Команда «{}»</b>\n\n<i>{}</i>",
        "command": "🌘 Команда «{}»",
        "button403": "Вы не можете нажать на эту кнопку!",
        "keep_id": "⚠️ Не удаляйте ID! {}",
        "choose_language": "🗽 <b>Выберите язык</b>",
        "not_official": (
            "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Этот язык не"
            " поддерживается официально</b>"
        ),
        "requested_join": (
            "💫 <b>Модуль</b> <code>{}</code> <b>запросил присоединение к каналу <a"
            " href='https://t.me/{}'>{}</a></b>\n\n<b>❓ Причина:</b> <i>{}</i>"
        ),
        "fw_error": (
            "<emoji document_id=5877458226823302157>🕒</emoji> <b>Команда"
            "</b> <code>{}</code> <b>вызвал FloodWait {} в методе</b> <code> {}</code>"
        ),
        "rpc_error": (
            "<emoji document_id=5877477244938489129>🚫</emoji> <b>Команда"
            "</b> <code>{}</code> <b>не удалась из-за ошибки RPC:</b>"
            " <code>{}</code>"
        ),
    }

    async def _change_language(self, call: InlineCall, lang: str):
        self._db.set(translations.__name__, "lang", lang)
        await self.allmodules.reload_translations()

        await call.edit(self.strings("lang_saved").format(self._get_flag(lang)))

    def _get_flag(self, lang: str) -> str:
        emoji_flags = {
            "🇬🇧": "<emoji document_id=6323589145717376403>🇬🇧</emoji>",
            "🇷🇺": "<emoji document_id=6323139226418284334>🇷🇺</emoji>",
        }

        lang2country = {"en": "🇬🇧"}

        lang = lang2country.get(lang) or utils.get_lang_flag(lang)
        return emoji_flags.get(lang, lang)

    @loader.command(ru_doc="[языки] - Изменить стандартный язык")
    async def setlang(self, message: Message):
        """[languages in the order of priority] - Change default language"""
        args = utils.get_args_raw(message)
        if not args:
            await self.inline.form(
                message=message,
                text=self.strings("choose_language"),
                reply_markup=utils.chunks(
                    [
                        {
                            "text": text,
                            "callback": self._change_language,
                            "args": (lang,),
                        }
                        for lang, text in SUPPORTED_LANGUAGES.items()
                    ],
                    2,
                ),
            )
            return

        if any(len(i) != 2 for i in args.split(" ")):
            await utils.answer(message, self.strings("incorrect_language"))
            return

        self._db.set(translations.__name__, "lang", args.lower())
        await self.allmodules.reload_translations()

        await utils.answer(
            message,
            self.strings("lang_saved").format(
                "".join([self._get_flag(lang) for lang in args.lower().split()])
            )
            + (
                ("\n\n" + self.strings("not_official"))
                if any(lang not in SUPPORTED_LANGUAGES for lang in args.lower().split())
                else ""
            ),
        )

    @loader.command(ru_doc="[ссылка на пак | пустое чтобы удалить] - Изменить внешний пак перевода")
    async def dllangpackcmd(self, message: Message):
        """[link to a langpack | empty to remove] - Change Netfoll translate pack (external)
        """
        args = utils.get_args_raw(message)

        if not args:
            self._db.set(translations.__name__, "pack", False)
            await self.translator.init()
            await utils.answer(message, self.strings("lang_removed"))
            return

        if not utils.check_url(args):
            await utils.answer(message, self.strings("check_url"))
            return

        self._db.set(translations.__name__, "pack", args)
        await utils.answer(
            message,
            self.strings(
                "pack_saved"
                if await self.allmodules.reload_translations()
                else "check_pack"
            ),
        )
