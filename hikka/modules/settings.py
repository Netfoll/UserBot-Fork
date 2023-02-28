# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

import os

import pyrogram
import telethon
from telethon.extensions.html import CUSTOM_EMOJIS
from telethon.tl.types import Message

from .. import loader, main, utils, version
from ..compat.dragon import DRAGON_EMOJI
from ..inline.types import InlineCall


@loader.tds
class CoreMod(loader.Module):
    """Control core userbot settings"""

    strings = {
        "name": "Settings",
        "too_many_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Too many args</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Chat {} blacklisted"
            " from userbot</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Chat {}"
            " unblacklisted from userbot</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>User {} blacklisted"
            " from userbot</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>User {}"
            " unblacklisted from userbot</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>❓</emoji> <b>What should the prefix"
            " be set to?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Prefix must be one"
            " symbol in length</b>"
        ),
        "prefix_set": (
            "{} <b>Command prefix"
            " updated. Type</b> <code>{newprefix}setprefix {oldprefix}</code> <b>to"
            " change it back</b>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Alias created."
            " Access it with</b> <code>{}</code>"
        ),
        "aliases": "<b>🔗 Aliases:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Command</b>"
            " <code>{}</code> <b>does not exist</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>You must provide a"
            " command and the alias for it</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>You must provide the"
            " alias name</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Alias</b>"
            " <code>{}</code> <b>removed</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Alias</b>"
            " <code>{}</code> <b>does not exist</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Database cleared</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>💜</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n"
            "<emoji document_id=5188666899860298925>🌒</emoji> <b>Hikka:</b> <i>V1.6.1</i>\n<emoji"
            " document_id=6327560044845991305>👾</emoji>"
            " <b>Developers: netfoll.t.me/3</b>"
        ),
        "confirm_cleardb": "⚠️ <b>Are you sure, that you want to clear database?</b>",
        "cleardb_confirm": "🗑 Clear database",
        "cancel": "🚫 Cancel",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>❓</emoji> <b>Who to blacklist?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>❓</emoji> <b>Who to"
            " unblacklist?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>🙈</emoji> <b>You are using an"
            " unstable branch</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>💣</emoji> <b>Your Dragon and Netfoll"
            " prefixes must be different!</b>"
        ),
    }

    strings_ru = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Слишком много"
            " аргументов</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Чат {} добавлен в"
            " черный список юзербота</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Чат {} удален из"
            " черного списка юзербота</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Пользователь {}"
            " добавлен в черный список юзербота</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Пользователь {}"
            " удален из черного списка юзербота</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>❓</emoji> <b>А какой префикс"
            " ставить то?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Префикс должен"
            " состоять только из одного символа</b>"
        ),
        "prefix_set": (
            "{} <b>Выставлен новый префикс,"
            " для того чтобы вернуть старый префикс используй</b> <code>{newprefix}setprefix"
            " {oldprefix}</code>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Алиас создан."
            " Используй его через</b> <code>{}</code>"
        ),
        "aliases": "<b>🔗 Алиасы:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Команда</b>"
            " <code>{}</code> <b>не существует</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Требуется ввести"
            " команду и алиас для нее</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Требуется имя"
            " алиаса</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Алиас</b>"
            " <code>{}</code> <b>удален</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Алиас</b>"
            " <code>{}</code> <b>не существует</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>База очищена</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>💜</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n"
            "<emoji document_id=5188666899860298925>🌒</emoji> <b>Hikka:</b> <i>V1.6.1</i>\n<emoji"
            " document_id=6327560044845991305>👾</emoji>"
            " <b>Разработчики: netfoll.t.me/3</b>"
        ),
        "_cls_doc": "Управление базовыми настройками юзербота",
        "confirm_cleardb": "⚠️ <b>Вы уверены, что хотите сбросить базу данных?</b>",
        "cleardb_confirm": "🗑 Очистить базу",
        "cancel": "🚫 Отмена",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>❓</emoji> <b>Кого заблокировать"
            " то?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>❓</emoji> <b>Кого разблокировать"
            " то?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=6334517075821725662>👀</emoji> <b>Используется"
            " нестабильная ветка</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>💣</emoji> <b>Префиксы Dragon и"
            " Netfoll должны отличаться!</b>"
        ),
    }

    strings_uk = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Надто много"
            " аргументов</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Чат {} додано в"
            " чорний список юзербота</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Чат {} видалено з"
            " чорного списку юзербота</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Користувач {}"
            " добавлен в чорний список юзербота</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Користувач {}"
            " удален из чорного списку юзербота</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>❓</emoji> <b>А який префікс"
            " ставити то?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Префікс повинен"
            " складатися тільки з одного символу</b>"
        ),
        "prefix_set": (
            "{} <b>Виставлено новий префікс,"
            " для того щоб повернути старий префікс використовуй</b> <code>{newprefix}setprefix"
            " {oldprefix}</code>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Аліас створений."
            " Використовуй його через</b> <code>{}</code>"
        ),
        "aliases": "<b>🔗 Аліаси:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Команда</b>"
            " <code>{}</code> <b>не існує</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Потрібно ввести"
            " команду і аліас для неї</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Потрібне ім'я"
            " алиаса</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>Аліас</b>"
            " <code>{}</code> <b>видаляти</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Аліас</b>"
            " <code>{}</code> <b>не існує</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>👍</emoji> <b>База очищена</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>💜</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n"
            "<emoji document_id=5188666899860298925>🌒</emoji> <b>Hikka:</b> <i>V1.6.1</i>\n<emoji"
            " document_id=6327560044845991305>👾</emoji>"
            " <b>Розробники: netfoll.t.me/3</b>"
        ),
        "_cls_doc": "Управління базовими настройками юзербота",
        "confirm_cleardb": "⚠️ <b>Ви впевнені, що хочете скинути базу даних?</b>",
        "cleardb_confirm": "🗑 Очистити базу",
        "cancel": "🚫 Скасування",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>❓</emoji> <b>Кого заблокувати"
            " то?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>❓</emoji> <b>Кого розблокувати"
            " то?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=6334517075821725662>👀</emoji> <b>Використовувати"
            " нестабільна гілка</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>💣</emoji> <b>Префікси Dragon і"
            " Netfoll повинні відрізнятися!</b>"
        ),
    }    

    async def blacklistcommon(self, message: Message):
        args = utils.get_args(message)

        if len(args) > 2:
            await utils.answer(message, self.strings("too_many_args"))
            return

        chatid = None
        module = None

        if args:
            try:
                chatid = int(args[0])
            except ValueError:
                module = args[0]

        if len(args) == 2:
            module = args[1]

        if chatid is None:
            chatid = utils.get_chat_id(message)

        module = self.allmodules.get_classname(module)
        return f"{str(chatid)}.{module}" if module else chatid

    @loader.command(
        ru_doc="Показать версию Netfoll",
    )
    async def netfollcmd(self, message: Message):
        """Get Netfoll version"""
        await utils.answer_file(
            message,
            "https://github.com/MXRRI/Netfoll/raw/stable/assets/banner.png",
            self.strings("hikka").format(
                (
                    (
                        utils.get_platform_emoji(self._client)
                        + (
                            ""
                            if "LAVHOST" in os.environ
                            else ""
                        )
                    )
                    if self._client.hikka_me.premium and CUSTOM_EMOJIS
                    else "👾 <b>Netfoll</b>"
                ),
                *version.netver,
                utils.get_commit_url(),
                f"{telethon.__version__} #{telethon.tl.alltlobjects.LAYER}",
                (
                    "<emoji document_id=5377399247589088543>🔥</emoji>"
                    if self._client.pyro_proxy
                    else "<emoji document_id=5418308381586759720>📴</emoji>"
                ),
                f"{pyrogram.__version__} #{pyrogram.raw.all.layer}",
            )
            + (
                ""
                if version.branch == "stable"
                else self.strings("unstable").format(version.branch)
            ),
        )

    @loader.command(
        ru_doc="[чат] [модуль] - Отключить бота где-либо",
    )
    async def blacklist(self, message: Message):
        """[chat_id] [module] - Blacklist the bot from operating somewhere"""
        chatid = await self.blacklistcommon(message)

        self._db.set(
            main.__name__,
            "blacklist_chats",
            self._db.get(main.__name__, "blacklist_chats", []) + [chatid],
        )

        await utils.answer(message, self.strings("blacklisted").format(chatid))

    @loader.command(
        ru_doc="[чат] - Включить бота где-либо",
    )
    async def unblacklist(self, message: Message):
        """<chat_id> - Unblacklist the bot from operating somewhere"""
        chatid = await self.blacklistcommon(message)

        self._db.set(
            main.__name__,
            "blacklist_chats",
            list(set(self._db.get(main.__name__, "blacklist_chats", [])) - {chatid}),
        )

        await utils.answer(message, self.strings("unblacklisted").format(chatid))

    async def getuser(self, message: Message):
        try:
            return int(utils.get_args(message)[0])
        except (ValueError, IndexError):
            reply = await message.get_reply_message()

            if reply:
                return reply.sender_id

            return message.to_id.user_id if message.is_private else False

    @loader.command(
        ru_doc="[пользователь] - Запретить пользователю выполнять команды",
    )
    async def blacklistuser(self, message: Message):
        """[user_id] - Prevent this user from running any commands"""
        user = await self.getuser(message)

        if not user:
            await utils.answer(message, self.strings("who_to_blacklist"))
            return

        self._db.set(
            main.__name__,
            "blacklist_users",
            self._db.get(main.__name__, "blacklist_users", []) + [user],
        )

        await utils.answer(message, self.strings("user_blacklisted").format(user))

    @loader.command(
        ru_doc="[пользователь] - Разрешить пользователю выполнять команды",
    )
    async def unblacklistuser(self, message: Message):
        """[user_id] - Allow this user to run permitted commands"""
        user = await self.getuser(message)

        if not user:
            await utils.answer(message, self.strings("who_to_unblacklist"))
            return

        self._db.set(
            main.__name__,
            "blacklist_users",
            list(set(self._db.get(main.__name__, "blacklist_users", [])) - {user}),
        )

        await utils.answer(
            message,
            self.strings("user_unblacklisted").format(user),
        )

    @loader.owner
    @loader.command(
        ru_doc="[dragon] <префикс> - Установить префикс команд",
    )
    async def setprefix(self, message: Message):
        """[dragon] <prefix> - Sets command prefix"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings("what_prefix"))
            return

        if len(args.split()) == 2 and args.split()[0] == "dragon":
            args = args.split()[1]
            is_dragon = True
        else:
            is_dragon = False

        if len(args) != 1:
            await utils.answer(message, self.strings("prefix_incorrect"))
            return

        if (
            not is_dragon
            and args[0] == self._db.get("dragon.prefix", "command_prefix", ",")
            or is_dragon
            and args[0] == self._db.get(main.__name__, "command_prefix", ".")
        ):
            await utils.answer(message, self.strings("prefix_collision"))
            return

        oldprefix = (
            f"dragon {self.get_prefix('dragon')}" if is_dragon else self.get_prefix()
        )
        self._db.set(
            "dragon.prefix" if is_dragon else main.__name__,
            "command_prefix",
            args,
        )
        await utils.answer(
            message,
            self.strings("prefix_set").format(
                (
                    DRAGON_EMOJI
                    if is_dragon
                    else "<emoji document_id=5370869711888194012>👾</emoji>"
                ),
                newprefix=utils.escape_html(
                    self.get_prefix() if is_dragon else args[0]
                ),
                oldprefix=utils.escape_html(oldprefix),
            ),
        )

    @loader.owner
    @loader.command(
        ru_doc="Показать список алиасов",
    )
    async def aliases(self, message: Message):
        """Print all your aliases"""
        aliases = self.allmodules.aliases
        string = self.strings("aliases")

        string += "\n".join(
            [f"▫️ <code>{i}</code> &lt;- {y}" for i, y in aliases.items()]
        )

        await utils.answer(message, string)

    @loader.owner
    @loader.command(
        ru_doc="Установить алиас для команды",
    )
    async def addalias(self, message: Message):
        """Set an alias for a command"""
        args = utils.get_args(message)

        if len(args) != 2:
            await utils.answer(message, self.strings("alias_args"))
            return

        alias, cmd = args
        if self.allmodules.add_alias(alias, cmd):
            self.set(
                "aliases",
                {
                    **self.get("aliases", {}),
                    alias: cmd,
                },
            )
            await utils.answer(
                message,
                self.strings("alias_created").format(utils.escape_html(alias)),
            )
        else:
            await utils.answer(
                message,
                self.strings("no_command").format(utils.escape_html(cmd)),
            )

    @loader.owner
    @loader.command(
        ru_doc="Удалить алиас для команды",
    )
    async def delalias(self, message: Message):
        """Remove an alias for a command"""
        args = utils.get_args(message)

        if len(args) != 1:
            await utils.answer(message, self.strings("delalias_args"))
            return

        alias = args[0]
        removed = self.allmodules.remove_alias(alias)

        if not removed:
            await utils.answer(
                message,
                self.strings("no_alias").format(utils.escape_html(alias)),
            )
            return

        current = self.get("aliases", {})
        del current[alias]
        self.set("aliases", current)
        await utils.answer(
            message,
            self.strings("alias_removed").format(utils.escape_html(alias)),
        )

    @loader.owner
    @loader.command(
        ru_doc="Очистить базу данных",
    )
    async def cleardb(self, message: Message):
        """Clear the entire database, effectively performing a factory reset"""
        await self.inline.form(
            self.strings("confirm_cleardb"),
            message,
            reply_markup=[
                {
                    "text": self.strings("cleardb_confirm"),
                    "callback": self._inline__cleardb,
                },
                {
                    "text": self.strings("cancel"),
                    "action": "close",
                },
            ],
        )

    async def _inline__cleardb(self, call: InlineCall):
        self._db.clear()
        self._db.save()
        await utils.answer(call, self.strings("db_cleared"))
