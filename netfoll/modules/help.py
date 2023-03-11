# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

import difflib
import inspect
import logging

from telethon.extensions.html import CUSTOM_EMOJIS
from telethon.tl.types import Message

from .. import loader, utils
from ..compat.dragon import DRAGON_EMOJI
from ..types import DragonModule

logger = logging.getLogger(__name__)


@loader.tds
class HelpMod(loader.Module):
    """Shows help for modules and commands"""

    strings = {
        "name": "Help",
        "undoc": "🦥 No docs",
        "support": (
            "{}\n\n <b>Link to</b> <a href='https://t.me/netfollUB'>support chat</a></b>"
        ),
        "not_exact": (
            "<emoji document_id=5312383351217201533>☝️</emoji> <b>No exact match"
            " occured, so the closest result is shown instead</b>"
        ),
        "request_join": "You requested link for Netfoll support chat",
        "core_notice": (
            "<emoji document_id=5312383351217201533>☝️</emoji> <b>This is a core"
            " module. You can't unload it nor replace</b>"
        ),
        "info": "<emoji document_id=6334760737906362392>⚡️</emoji><b> You didn't specify a module to search for</b>\n\n<i>The installed modules can be viewed in</i> <code>{}mods</code>"
    }

    strings_ru = {
        "undoc": "🦥 Нет описания",
        "support": (
            "{}\n\n <b>Ссылка на</b> <a href='https://t.me/netfollUB'>чат помощи</a></b>"
        ),
        "_cls_doc": "Показывает помощь по модулям",
        "not_exact": (
            "<emoji document_id=5312383351217201533>☝️</emoji> <b>Точного совпадения"
            " не нашлось, поэтому было выбрано наиболее подходящее</b>"
        ),
        "request_join": "Вы запросили ссылку на чат помощи Netfoll",
        "core_notice": (
            "<emoji document_id=6328010818843575869>ℹ️</emoji> <b>Это встроенный"
            " модуль. Вы не можете его выгрузить или заменить</b>"
        ),
        "info": "<emoji document_id=6334760737906362392>⚡️</emoji><b> Вы не указали модуль для поиска</b>\n\n<i>Установленные модули можно посмотреть в</i> <code>{}mods</code>"
    }

    strings_uk = {
        "undoc": "🦥 Немає опису",
        "support": (
            "{}\n\n <b>Посилання на</b> <a href='https://t.me/netfollUB'>чат допомоги</a></b>"
        ),
        "_cls_doc": "Показує допомогу по модулях",
        "not_exact": (
            "<emoji document_id=5312383351217201533>☝️</emoji> <b>Точного збігу"
            " не знайшлося, тому було вибрано найбільш підходяще</b>"
        ),
        "request_join": "Ви запросили посилання на чат допомоги Netfoll",
        "core_notice": (
            "<emoji document_id=6328010818843575869>ℹ️</emoji> <b>Це вбудований"
            " модуль. Ви не можете його вивантажити або замінити</b>"
        ),
        "info": "<emoji document_id=6334760737906362392>⚡️</emoji><b> Ви не вказали модуль для пошуку</b>\n\n<i>Встановлені модулі можна подивитися в</i> <code>{}mods</code>"
    }

    def find_aliases(self, command: str) -> list:
        """Find aliases for command"""
        aliases = []
        _command = self.allmodules.commands[command]
        if getattr(_command, "alias", None) and not (
            aliases := getattr(_command, "aliases", None)
        ):
            aliases = [_command.alias]

        return aliases or []

    async def modhelp(self, message: Message, args: str):
        exact = True
        module = self.lookup(args, include_dragon=True)

        if not module:
            cmd = args.lower().strip(self.get_prefix())
            if method := self.allmodules.dispatch(cmd)[1]:
                module = method.__self__

        if not module:
            module = self.lookup(
                next(
                    (
                        reversed(
                            sorted(
                                [
                                    module.strings["name"]
                                    for module in self.allmodules.modules
                                ],
                                key=lambda x: difflib.SequenceMatcher(
                                    None,
                                    args.lower(),
                                    x,
                                ).ratio(),
                            )
                        )
                    ),
                    None,
                )
            )

            exact = False

        is_dragon = isinstance(module, DragonModule)

        try:
            name = module.strings("name")
        except (KeyError, AttributeError):
            name = getattr(module, "name", "ERROR")

        _name = (
            "{} (v{}.{}.{})".format(
                utils.escape_html(name),
                module.__version__[0],
                module.__version__[1],
                module.__version__[2],
            )
            if hasattr(module, "__version__")
            else utils.escape_html(name)
        )

        reply = "{} <b>{}</b>:".format(
            (
                DRAGON_EMOJI
                if is_dragon
                else "<emoji document_id=5370869711888194012>👾</emoji>"
            ),
            _name,
        )
        if module.__doc__:
            reply += (
                "<i>\n<emoji document_id=5255841103197775720>ℹ️</emoji> "
                + utils.escape_html(inspect.getdoc(module))
                + "\n</i>"
            )

        commands = (
            module.commands
            if is_dragon
            else {
                name: func
                for name, func in module.commands.items()
                if await self.allmodules.check_security(message, func)
            }
        )

        if hasattr(module, "inline_handlers") and not is_dragon:
            for name, fun in module.inline_handlers.items():
                reply += (
                    "\n<emoji document_id=5372981976804366741>🤖</emoji>"
                    " <code>{}</code> {}".format(
                        f"@{self.inline.bot_username} {name}",
                        (
                            utils.escape_html(inspect.getdoc(fun))
                            if fun.__doc__
                            else self.strings("undoc")
                        ),
                    )
                )

        for name, fun in commands.items():
            reply += (
                "\n<emoji document_id=5256034020243809941>▫️</emoji>"
                " <code>{}{}</code>{} {}".format(
                    self.get_prefix("dragon" if is_dragon else None),
                    name,
                    " ({})".format(
                        ", ".join(
                            "<code>{}{}</code>".format(
                                self.get_prefix("dragon" if is_dragon else None), alias
                            )
                            for alias in self.find_aliases(name)
                        )
                    )
                    if self.find_aliases(name)
                    else "",
                    utils.escape_html(fun)
                    if is_dragon
                    else (
                        utils.escape_html(inspect.getdoc(fun))
                        if fun.__doc__
                        else self.strings("undoc")
                    ),
                )
            )

        await utils.answer(
            message,
            reply
            + (f"\n\n{self.strings('not_exact')}" if not exact else "")
            + (
                f"\n\n{self.strings('core_notice')}"
                if module.__origin__.startswith("<core")
                else ""
            ),
        )

    @loader.unrestricted
    @loader.command(ru_doc="[модуль] [-f] - Показать помощь",)
    async def help(self, message: Message):
        """[module] [-f] - Show help"""
        args = utils.get_args_raw(message)
        prefix = f"{self.strings('info').format(str(self.get_prefix()))}\n"
        if "-f" in args:
            args = args.replace(" -f", "").replace("-f", "")

        if args:
            await self.modhelp(message, args)
            return

        await utils.answer(message, prefix)

    @loader.command(ru_doc="Показать ссылку на чат помощи Netfoll")
    async def support(self, message):
        """Get link of Netfoll support chat"""
        if message.out:
            await self.request_join("@netfolub", self.strings("request_join"))

        await utils.answer(
            message,
            self.strings("support").format(
                (
                    utils.get_platform_emoji(self._client)
                    if self._client.hikka_me.premium and CUSTOM_EMOJIS
                    else "👾"
                )
            ),
        )
