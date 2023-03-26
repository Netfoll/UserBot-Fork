# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import inspect
import logging
import os
import time
import typing
from io import BytesIO

from telethon.tl.types import Message

from .. import loader, main, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds
class TestMod(loader.Module):
    """Perform operations based on userbot self-testing"""

    _memory = {}

    strings = {
        "name": "Tester",
        "set_loglevel": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Please specify"
            " verbosity as an integer or string</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>🤷‍♀️</emoji> <b>You don't have any"
            " logs at verbosity</b> <code>{}</code><b>.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5384307092599348179>🫡</emoji> <b>Netfoll logs with"
            " verbosity</b> <code>{}</code>\n\n<emoji"
            " document_id=6318902906900711458>⚪️</emoji> <b>Version:"
            " {}.{}.{}</b>{}"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Invalid time to"
            " suspend</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>🥶</emoji> <b>Bot suspended"
            " for</b> <code>{}</code> <b>seconds</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>⚡️</emoji> <b>Telegram ping:</b>"
            " <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>🚀</emoji> <b>Uptime: {}</b>"
        ),
        "confidential": (
            "⚠️ <b>Log level</b> <code>{}</code> <b>may reveal your confidential info,"
            " be careful</b>"
        ),
        "confidential_text": (
            "⚠️ <b>Log level</b> <code>{0}</code> <b>may reveal your confidential info,"
            " be careful</b>\n<b>Type</b> <code>.logs {0} force_insecure</code> <b>to"
            " ignore this warning</b>"
        ),
        "choose_loglevel": "💁‍♂️ <b>Choose log level</b>",
        "bad_module": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Module not found</b>"
        ),
        "debugging_enabled": (
            "<emoji document_id=5332533929020761310>✅</emoji> <b>Debugging mode enabled"
            " for module</b> <code>{0}</code>\n<i>Go to directory named"
            " `debug_modules`, edit file named `{0}.py` and see changes in real"
            " time</i>"
        ),
        "debugging_disabled": (
            "<emoji document_id=5332533929020761310>✅</emoji> <b>Debugging disabled</b>"
        ),
        "send_anyway": "📤 Send anyway",
        "cancel": "🚫 Cancel",
        "logs_cleared": "🗑 <b>Logs cleared</b>",
    }

    strings_ru = {
        "set_loglevel": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Укажи уровень логов"
            " числом или строкой</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>🤷‍♀️</emoji> <b>У тебя нет логов"
            " уровня</b> <code>{}</code><b>.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5384307092599348179>🫡</emoji> Логи <b>Netfoll</b> уровня"
            "</b> <code>{}</code>\n\n<emoji document_id=6318902906900711458>⚪️</emoji>"
            " <b>Версия: {}.{}.{}</b>{}"
        ),
        "debugging_enabled": (
            "<emoji document_id=5332533929020761310>✅</emoji> <b>Режим разработчика"
            " включен для модуля</b> <code>{0}</code>\n<i>Отправляйся в директорию"
            " `debug_modules`, изменяй файл `{0}.py`, и смотри изменения в режиме"
            " реального времени</i>"
        ),
        "debugging_disabled": (
            "<emoji document_id=5332533929020761310>✅</emoji> <b>Режим разработчика"
            " выключен</b>"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Неверное время"
            " заморозки</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>🥶</emoji> <b>Бот заморожен на</b>"
            " <code>{}</code> <b>секунд</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>⚡️</emoji> <b>Скорость отклика"
            " Telegram:</b> <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>🚀</emoji> <b>Прошло с последней"
            " перезагрузки: {}</b>"
        ),
        "confidential": (
            "⚠️ <b>Уровень логов</b> <code>{}</code> <b>может содержать личную"
            " информацию, будь осторожен</b>"
        ),
        "confidential_text": (
            "⚠️ <b>Уровень логов</b> <code>{0}</code> <b>может содержать личную"
            " информацию, будь осторожен</b>\n<b>Напиши</b> <code>.logs {0}"
            " force_insecure</code><b>, чтобы отправить логи игнорируя"
            " предупреждение</b>"
        ),
        "choose_loglevel": "💁‍♂️ <b>Выбери уровень логов</b>",
        "_cmd_doc_dump": "Показать информацию о сообщении",
        "_cmd_doc_logs": (
            "<уровень> - Отправляет лог-файл. Уровни ниже WARNING могут содержать"
            " личную инфомрацию."
        ),
        "_cmd_doc_suspend": "<время> - Заморозить бота на некоторое время",
        "_cmd_doc_ping": "Проверяет скорость отклика юзербота",
        "_cls_doc": "Операции, связанные с самотестированием",
        "send_anyway": "📤 Все равно отправить",
        "cancel": "🚫 Отмена",
        "logs_cleared": "🗑 <b>Логи очищены</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "force_send_all",
                False,
                "⚠️ Do not touch, if you don't know what it does!\nBy default, Netfoll"
                " will try to determine, which client caused logs. E.g. there is a"
                " module TestModule installed on Client1 and TestModule2 on Client2. By"
                " default, Client2 will get logs from TestModule2, and Client1 will get"
                " logs from TestModule. If this option is enabled, Netfoll will send all"
                " logs to Client1 and Client2, even if it is not the one that caused"
                " the log.",
                validator=loader.validators.Boolean(),
                on_change=self._pass_config_to_logger,
            ),
            loader.ConfigValue(
                "tglog_level",
                "INFO",
                "⚠️ Do not touch, if you don't know what it does!\n"
                "Minimal loglevel for records to be sent in Telegram.",
                validator=loader.validators.Choice(
                    ["INFO", "WARNING", "ERROR", "CRITICAL"]
                ),
                on_change=self._pass_config_to_logger,
            ),
        )

    def _pass_config_to_logger(self):
        logging.getLogger().handlers[0].force_send_all = self.config["force_send_all"]
        logging.getLogger().handlers[0].tg_level = {
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50,
        }[self.config["tglog_level"]]

    @loader.command(ru_doc="Ответь на сообщение, чтобы показать его дамп")
    async def dump(self, message: Message):
        """Use in reply to get a dump of a message"""
        if not message.is_reply:
            return

        await utils.answer(
            message,
            "<code>"
            + utils.escape_html((await message.get_reply_message()).stringify())
            + "</code>",
        )

    @loader.command(ru_doc="Очистить логи")
    async def clearlogs(self, message: Message):
        """Clear logs"""
        for handler in logging.getLogger().handlers:
            handler.buffer = []
            handler.handledbuffer = []
            handler.tg_buff = ""

        await utils.answer(message, self.strings("logs_cleared"))

    @loader.command(ru_doc="<уровень> - Показать логи")
    async def logs(
        self,
        message: typing.Union[Message, InlineCall],
        force: bool = False,
        lvl: typing.Union[int, None] = None,
    ):
        """<level> - Dump logs"""
        if not isinstance(lvl, int):
            args = utils.get_args_raw(message)
            try:
                try:
                    lvl = int(args.split()[0])
                except ValueError:
                    lvl = getattr(logging, args.split()[0].upper(), None)
            except IndexError:
                lvl = None

        if not isinstance(lvl, int):
            try:
                if not self.inline.init_complete or not await self.inline.form(
                    text=self.strings("choose_loglevel"),
                    reply_markup=utils.chunks(
                        [
                            {
                                "text": name,
                                "callback": self.logs,
                                "args": (False, level),
                            }
                            for name, level in [
                                ("🚫 Error", 40),
                                ("⚠️ Warning", 30),
                                ("ℹ️ Info", 20),
                                ("🧑‍💻 All", 0),
                            ]
                        ],
                        2,
                    )
                    + [[{"text": self.strings("cancel"), "action": "close"}]],
                    message=message,
                ):
                    raise
            except Exception:
                await utils.answer(message, self.strings("set_loglevel"))

            return

        logs = "\n\n".join(
            [
                "\n".join(
                    handler.dumps(lvl, client_id=self._client.tg_id)
                    if "client_id" in inspect.signature(handler.dumps).parameters
                    else handler.dumps(lvl)
                )
                for handler in logging.getLogger().handlers
            ]
        )

        named_lvl = (
            lvl
            if lvl not in logging._levelToName
            else logging._levelToName[lvl]  # skipcq: PYL-W0212
        )

        if (
            lvl < logging.WARNING
            and not force
            and (
                not isinstance(message, Message)
                or "force_insecure" not in message.raw_text.lower()
            )
        ):
            try:
                if not self.inline.init_complete:
                    raise

                cfg = {
                    "text": self.strings("confidential").format(named_lvl),
                    "reply_markup": [
                        {
                            "text": self.strings("send_anyway"),
                            "callback": self.logs,
                            "args": [True, lvl],
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                }
                if isinstance(message, Message):
                    if not await self.inline.form(**cfg, message=message):
                        raise
                else:
                    await message.edit(**cfg)
            except Exception:
                await utils.answer(
                    message,
                    self.strings("confidential_text").format(named_lvl),
                )

            return

        if len(logs) <= 2:
            if isinstance(message, Message):
                await utils.answer(message, self.strings("no_logs").format(named_lvl))
            else:
                await message.edit(self.strings("no_logs").format(named_lvl))
                await message.unload()

            return

        logs = self.lookup("python").censor(logs)

        logs = BytesIO(logs.encode("utf-16"))
        logs.name = "netfoll-logs.txt"

        ghash = utils.get_git_hash()

        other = (
            *main.netver,
            (
                " <a"
                f' href="https://github.com/MXRRI/Netfoll/commit/{ghash}">@{ghash[:8]}</a>'
                if ghash
                else ""
            ),
        )

        if getattr(message, "out", True):
            await message.delete()

        if isinstance(message, Message):
            await utils.answer(
                message,
                logs,
                caption=self.strings("logs_caption").format(named_lvl, *other),
            )
        else:
            await self._client.send_file(
                message.form["chat"],
                logs,
                caption=self.strings("logs_caption").format(named_lvl, *other),
                reply_to=message.form["top_msg_id"],
            )

    @loader.owner
    @loader.command(ru_doc="<время> - Заморозить бота на N секунд")
    async def suspend(self, message: Message):
        """<time> - Suspends the bot for N seconds"""
        try:
            time_sleep = float(utils.get_args_raw(message))
            await utils.answer(
                message,
                self.strings("suspended").format(time_sleep),
            )
            time.sleep(time_sleep)
        except ValueError:
            await utils.answer(message, self.strings("suspend_invalid_time"))

    @loader.command(ru_doc="Проверить скорость отклика юзербота")
    async def ping(self, message: Message):
        """Test your userbot ping"""
        start = time.perf_counter_ns()
        message = await utils.answer(message, "👾")

        await utils.answer(
            message,
            self.strings("results_ping").format(
                round((time.perf_counter_ns() - start) / 10**6, 3),
                utils.formatted_uptime(),
            ),
        )

    async def client_ready(self):
        chat, _ = await utils.asset_channel(
            self._client,
            "netfoll-logs",
            "👾 Your Netfoll logs will appear in this chat",
            silent=True,
            invite_bot=True,
            avatar="https://github.com/MXRII/Netfoll/assets/raw/master/logs.jpg",
        )

        self._logchat = int(f"-100{chat.id}")

        logging.getLogger().handlers[0].install_tg_log(self)
        logger.debug("Bot logging installed for %s", self._logchat)

        self._pass_config_to_logger()
