# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: inline_bot_manager
# Description: Control over your Inline bot!
# Author: Den4ikSuperOstryyPer4ik
# Commands:
# .inlinebothelp | .ibsetname | .ibsetqtext | .ibsetdescription | .ibsetabout
# .ibcheckname
# ---------------------------------------------------------------------------------


#               _             __  __           _       _
#     /\       | |           |  \/  |         | |     | |
#    /  \   ___| |_ _ __ ___ | \  / | ___   __| |_   _| | ___  ___
#   / /\ \ / __| __| '__/ _ \| |\/| |/ _ \ / _` | | | | |/ _ \/ __|
#  / ____ \\__ \ |_| | | (_) | |  | | (_) | (_| | |_| | |  __/\__ \
# /_/    \_\___/\__|_|  \___/|_|  |_|\___/ \__,_|\__,_|_|\___||___/
#
#               © Copyright 2022
#
#      https://t.me/Den4ikSuperOstryyPer4ik
#                      and
#             https://t.me/ToXicUse
#
#       🔒 Licensed under the GNU AGPLv3
#    https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @AstroModules
# meta pic: https://img.icons8.com/plasticine/200/000000/bot.png
# meta banner: еще нету :(
# scope: hikka_only
# scope: hikka_min 1.3.0

import logging

from .. import loader
from .. import utils as u

logger = logging.getLogger(__name__)


@loader.tds
class InlineBotManagerMod(loader.Module):
    """Control over your Inline bot!"""

    strings = {
        "name": "InlineBotManager",
        "no_args": (
            "No arguments :( | Read, how to use the module, command: <code>{}>/code>"
        ),
        "...-set": (
            "<b>{} for your inline bot(@{}) successfully set to <code>{}</code></b>"
        ),
        "error": "An error has occurred.",
        "namea": "Name",
        "inline-text": "Inline-Text",
        "about-text": "About",
        "description-text": "Description",
        "help-mod": """<b><i>•<u>Instructions for the module:</u>
------------------------------------------------
•<u>Information about the module:</u>
    •Module name --> <code>InlineBotManager</code>
    •Module description --> <code>Control over your Inline bot!</code>
    •Link to the module(to download) --> <code></code>
    •Unload the module --> <code>{prefix}unloadmod InlineBotManager</code>
    •Your inline botname --> <code>{}</code>
    •Your inline bot username --> @{}
------------------------------------------------
• Commands:
    • <code>{prefix}ibcheckname</code> --> check bot name to be: "<code>🌘 Hikka Userbot of {your nickname}</code>"
    --------------------------------------------
    • <code>{prefix}ibsetname </code><name> --> set a name for your Inline Bot
    Command example:
    <code>{prefix}ibsetname DSOP-UserBot</code>
    --------------------------------------------
    • <code>{prefix}ibsetqtext </code><text> --> set text instead of "InlineQuery" for your Inline Bot
    Command example:
    <code>{prefix}ibsetqtext UserBot-Inline-Query</code>
    --------------------------------------------
    • <code>{prefix}ibsetdescription </code><text> --> change the information Description the inline bot
    Command example:
    <code>{prefix}ibsetdescription DSOP-UserBot</code>
    --------------------------------------------
    • <code>{prefix}ibsetabout </code><text> --> change the text about the information about the inline bot
    Command example:
    <code>{prefix}ibsetabout DSOP-UserBot-about</code>
------------------------------------------------</i></b>""",
        "check-yes": "<b>Bot name checked successfully!\nIt's correct.</b>",
        "check-no": (
            "<b>Your inline bot name(@{}) was successfully checked! Result: bot name"
            " didn't match account name, bot name was changed from <code>{}</code> to"
            " <code>{}</code></b>"
        ),
        "_cfg_check_name": (
            "Check and change the name of your inline bot after every restart?"
        ),
    }

    strings_ru = {
        "_cls_doc": """Управление над своим Inline ботом!""",
        "no_args": (
            "Нет аргументов :( | Прочитайте, как пользоваться модулем, командой:"
            " <code>{}</code>"
        ),
        "...-set": (
            "<b>{} для вашего инлайн-бота(@{}) успешно установлен(-о/-а) на"
            " <code>{}</code></b>"
        ),
        "namea": "Имя",
        "inline-text": "Inline-Текст",
        "about-text": "Текст об информации",
        "description-text": "Информация",
        "error": "Произошла ошибка.",
        "help-mod": """<b><i>•<u>Инструкция к модулю:</u>
------------------------------------------------
•<u>Информация о модуле:</u>
    •Название модуля --> <code>InlineBotManager</code>
    •Описание модуля --> <code>Управление над своим Inline ботом!</code>
    •Ссылка на модуль(для загрузки) --> <code></code>
    •Выгрузить модуль --> <code>{prefix}unloadmod InlineBotManager</code>
------------------------------------------------
•Информация о вашем Инлайн-Боте:
    ------
    •Имя бота --> <code>{}</code>
    ----------------------
    •Юзернейм бота --> @{}
------------------------------------------------
•Команды:
    • <code>{prefix}ibcheckname</code> --> проверить имя бота, чтобы оно было: "🌘 Hikka Userbot of (ваш ник-нейм)"
------------------------------------------------
    • <code>{prefix}ibsetname </code><имя> --> установить имя для вашего Инлайн-Бота
    Пример команды:
    <code>{prefix}ibsetname DSOP-UserBot</code>
------------------------------------------------
    • <code>{prefix}ibsetqtext </code><текст> --> установить текст вместо "InlineQuery" для вашего Инлайн-Бота
    Пример команды:
    <code>{prefix}ibsetqtext UserBot-Inline-Query</code>
------------------------------------------------
    • <code>{prefix}ibsetdescription </code><текст> --> изменить информацию о инлайн-боте
    Пример команды:
    <code>{prefix}ibsetdescription DSOP-UserBot</code>
------------------------------------------------
    • <code>{prefix}ibsetabout </code><текст> --> изменить текст об информации о инлайн-боте
    Пример команды:
    <code>{prefix}ibsetabout DSOP-UserBot-about</code>
------------------------------------------------</i></b>""",
        "ib-help": """<b>----------------------
</b>""",
        "check-yes": "<b>Имя бота успешно проверено!\nОно верное.</b>",
        "check-no": (
            "<b>Имя вашего инлайн-бота(@{}) было успешно проверено! Результат: имя бота"
            " не соответствовало имени аккаунта, имя бота было сменено с"
            " <code>{}</code> на <code>{}</code></b>"
        ),
        "_cfg_check_name": (
            "Проверять и изменять имя вашего инлайн-бота после каждого рестарта?"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "check_name",
                False,
                lambda: self.strings("_cfg_check_name"),
                validator=loader.validators.Boolean(),
            )
        )

    @loader.command(ru_doc="--> Просмотреть помощь по этому модулю")
    async def inlinebothelpcmd(self, message):
        """--> Check help for this module"""
        await message.delete()
        name = self.bot.first_name
        username = self.bot.username
        await self.client.send_message(
            message.peer_id,
            self.strings("help-mod").format(
                name,
                username,
                prefix=self.get_prefix(),
            ),
        )

    @loader.command(ru_doc="<имя> --> изменить имя для вашего Инлайн-Бота")
    async def ibsetnamecmd(self, message):
        """<name> --> change Name for your Inline-Bot"""
        args = u.get_args_raw(message)
        if not args:
            command = f"{self.get_prefix()}inlinebothelp"
            await u.answer(message, self.strings("no_args").format(command))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setname")
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.send_message(args)
                await conv.mark_read()

            await u.answer(
                message,
                self.strings("...-set").format(
                    self.strings("namea"), self.inline.bot_username, args
                ),
            )

    @loader.command(
        ru_doc="<текст> --> изменить текст в InlineQuery для вашего Инлайн-Бота"
    )
    async def ibsetqtextcmd(self, message):
        """<text> --> change text in InlineQuery for your Inline-Bot"""
        args = u.get_args_raw(message)
        if not args:
            command = f"{self.get_prefix()}inlinebothelp"
            await u.answer(message, self.strings("no_args").format(command))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setinline")
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.send_message(args)
                await conv.mark_read()

            await u.answer(
                message,
                self.strings("...-set").format(
                    self.strings("inline-text"), self.inline.bot_username, args
                ),
            )

    @loader.command(ru_doc="<текст> --> изменить информацию о инлайн-боте")
    async def ibsetdescriptioncmd(self, message):
        """<description> --> change inline-bot description"""
        args = u.get_args_raw(message)
        if not args:
            command = f"{self.get_prefix()}inlinebothelp"
            await u.answer(message, self.strings("no_args").format(command))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setdescription")
                await conv.mark_read()
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.mark_read()
                await conv.send_message(args)
            await u.answer(
                message,
                self.strings("...-set").format(
                    self.strings("description-text"), self.inline.bot_username, args
                ),
            )

    @loader.command(ru_doc="<текст> --> изменить текст об информации о инлайн-боте")
    async def ibsetaboutcmd(self, message):
        """<about> --> change inline-bot about text"""
        args = u.get_args_raw(message)
        if not args:
            command = f"{self.get_prefix()}inlinebothelp"
            await u.answer(message, self.strings("no_args").format(command))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setabouttext")
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.send_message(args)
                await conv.mark_read()

            await u.answer(
                message,
                self.strings("...-set").format(
                    self.strings("about-text"), self.inline.bot_username, args
                ),
            )

    @loader.command(
        ru_doc="""-->проверить имя бота, чтобы оно было: "🌘 Hikka Userbot of {ваш ник}" """
    )
    async def ibchecknamecmd(self, message):
        """-->check bot name to be: "🌘 Hikka Userbot of {your nickname}" """
        bot_name = self.bot.first_name
        acc_name = self.acc.first_name
        norm_nameb = f"🌘 Hikka Userbot of {acc_name}"
        if bot_name == norm_nameb:
            await u.answer(message, self.strings("check-yes"))
            logger.debug(self.strings("check-yes"))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setname")
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.send_message(norm_nameb)
                await conv.mark_read()

            logger.info(
                self.strings("check-no").format(self.bot.username, bot_name, norm_nameb)
            )
            await u.answer(
                message,
                self.strings("check-no").format(
                    self.inline.bot_username, bot_name, norm_nameb
                ),
            )

    async def client_ready(self, *_):
        self.botfather = "@BotFather"
        self.bot = await self.inline.bot.get_me()
        self.acc = await self.client.get_me()
        if self.config["check_name"]:
            m = await self.client.send_message("me", f"{self.get_prefix()}ibcheckname")
            await self.ibchecknamecmd(m)
