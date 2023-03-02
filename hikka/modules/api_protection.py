# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

import asyncio
import io
import json
import logging
import random
import time

from telethon.tl import functions
from telethon.tl.tlobject import TLRequest
from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import InlineCall
from ..web.debugger import WebDebugger

logger = logging.getLogger(__name__)

GROUPS = [
    "auth",
    "account",
    "users",
    "contacts",
    "messages",
    "updates",
    "photos",
    "upload",
    "help",
    "channels",
    "bots",
    "payments",
    "stickers",
    "phone",
    "langpack",
    "folders",
    "stats",
]


CONSTRUCTORS = {
    (lambda x: x[0].lower() + x[1:])(
        method.__class__.__name__.rsplit("Request", 1)[0]
    ): method.CONSTRUCTOR_ID
    for method in utils.array_sum(
        [
            [
                method
                for method in dir(getattr(functions, group))
                if isinstance(method, TLRequest)
            ]
            for group in GROUPS
        ]
    )
}


@loader.tds
class APIRatelimiterMod(loader.Module):
    """Helps userbot avoid spamming Telegram API"""

    strings = {
        "name": "APILimiter",
        "warning": (
            "<emoji document_id=5312383351217201533>⚠️</emoji>"
            " <b>WARNING!</b>\n\nYour account exceeded the limit of requests, specified"
            " in config. In order to prevent Telegram API Flood, userbot has been"
            " <b>fully frozen</b> for {} seconds. Further info is provided in attached"
            " file. \n\nIt is recommended to get help in <code>{prefix}support</code>"
            " group!\n\nIf you think, that it is an intended behavior, then wait until"
            " userbot gets unlocked and next time, when you will be going to perform"
            " such an operation, use <code>{prefix}suspend_api_protect</code> &lt;time"
            " in seconds&gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Invalid arguments</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>👌</emoji> <b>API Flood Protection"
            " is disabled for {} seconds</b>"
        ),
        "on": (
            "<emoji document_id=5458450833857322148>👌</emoji> <b>Protection enabled</b>"
        ),
        "off": (
            "<emoji document_id=5458450833857322148>👌</emoji> <b>Protection"
            " disabled</b>"
        ),
        "u_sure": "⚠️ <b>Are you sure?</b>",
        "_cfg_time_sample": "Time sample through which the bot will count requests",
        "_cfg_threshold": "Threshold of requests to trigger protection",
        "_cfg_local_floodwait": (
            "Freeze userbot for this amount of time, if request limit exceeds"
        ),
        "_cfg_forbidden_methods": (
            "Forbid specified methods from being executed throughout external modules"
        ),
        "btn_no": "🚫 No",
        "btn_yes": "✅ Yes",
        "web_pin": (
            "🔓 <b>Click the button below to show Werkzeug debug PIN. Do not give it to"
            " anyone.</b>"
        ),
        "web_pin_btn": "🐞 Show Werkzeug PIN",
        "proxied_url": "🌐 Proxied URL",
        "local_url": "🏠 Local URL",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Web debugger is"
            " disabled, url is not available</b>"
        ),
    }

    strings_ru = {
        "warning": (
            "<emoji document_id=5312383351217201533>⚠️</emoji>"
            " <b>ВНИМАНИЕ!</b>\n\nАккаунт вышел за лимиты запросов, указанные в"
            " конфиге. С целью предотвращения флуда Telegram API, юзербот был"
            " <b>полностью заморожен</b> на {} секунд. Дополнительная информация"
            " прикреплена в файле ниже. \n\nРекомендуется обратиться за помощью в"
            " <code>{prefix}support</code> группу!\n\nЕсли ты считаешь, что это"
            " запланированное поведение юзербота, просто подожди, пока закончится"
            " таймер и в следующий раз, когда запланируешь выполнять такую"
            " ресурсозатратную операцию, используй"
            " <code>{prefix}suspend_api_protect</code> &lt;время в секундах&gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Неверные аргументы</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>👌</emoji> <b>Защита API отключена"
            " на {} секунд</b>"
        ),
        "on": "<emoji document_id=5458450833857322148>👌</emoji> <b>Защита включена</b>",
        "off": (
            "<emoji document_id=5458450833857322148>👌</emoji> <b>Защита отключена</b>"
        ),
        "u_sure": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Ты уверен?</b>",
        "_cfg_time_sample": (
            "Временной промежуток, по которому будет считаться количество запросов"
        ),
        "_cfg_threshold": "Порог запросов, при котором будет срабатывать защита",
        "_cfg_local_floodwait": (
            "Заморозить юзербота на это количество секунд, если лимит запросов превышен"
        ),
        "_cfg_forbidden_methods": (
            "Запретить выполнение указанных методов во всех внешних модулях"
        ),
        "btn_no": "🚫 Нет",
        "btn_yes": "✅ Да",
        "web_pin": (
            "🔓 <b>Нажми на кнопку ниже, чтобы показать Werkzeug debug PIN. Не давай его"
            " никому.</b>"
        ),
        "web_pin_btn": "🐞 Показать Werkzeug PIN",
        "proxied_url": "🌐 Проксированная ссылка",
        "local_url": "🏠 Локальная ссылка",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Веб-отладчик отключен,"
            " ссылка недоступна</b>"
        ),
    }

    strings_uk = {
        "warning": (
            "<emoji document_id=5312383351217201533>⚠️</emoji>"
            "<b> увага!</b>\n\N Аккаунт вийшов за ліміти запитів, зазначені в"
            "конфіге. З метою запобігання флуду Telegram API, юзербот був"
            "<b> повністю заморожений</b> На {} секунд. Додаткова інформація"
            "прикріплена у файлі нижче. \n\n предкомендуется звернутися за допомогою в"
            "<code>{prefix}support</code> групу!\n\n пякщо ти вважаєш, що це"
            "запланована поведінка юзербота, просто почекай, поки закінчиться"
            "таймер і наступного разу, коли заплануєш виконувати таку"
            "ресурсовитратну операцію, використовуй"
            "<code> {prefix}suspend_api_protect</code> &LT; час у секундах &gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Невірні аргументи</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>👌</emoji> <b>Захист API вимкнено"
            " на {} секунд</b>"
        ),
        "on": "<emoji document_id=5458450833857322148>👌</emoji> <b>Захист включена</b>",
        "off": (
            "<emoji document_id=5458450833857322148>👌</emoji> <b>Захист відключений</b>"
        ),
        "u_sure": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Ти впевнений?</b>",
        "_cfg_time_sample": (
            "Часовий проміжок, за яким буде вважатися кількість запитів"
        ),
        "_cfg_threshold": "Поріг запитів, при якому буде спрацьовувати захист",
        "_cfg_local_floodwait": (
            "Заморозити юзербота на цю кількість секунд, якщо ліміт запитів перевищено"
        ),
        "_cfg_forbidden_methods": (
            "Заборонити виконання зазначених методів у всіх зовнішніх модулях"
        ),
        "btn_no": "🚫 Ні",
        "btn_yes": "✅ Так",
        "web_pin": (
            "🔓 <b>Натисни на кнопку нижче, щоб показати Werkzeug Debug PIN. Не давай його"
            " никому.</b>"
        ),
        "web_pin_btn": "🐞 Показать показати Werkzeug PIN",
        "proxied_url": "🌐 Gрок проксі-посилання",
        "local_url": " 🏠 Локальне посилання",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Веб-налагоджувач вимкнено,"
            " посилання недоступне</b>"
        ),
    }

    _ratelimiter = []
    _suspend_until = 0
    _lock = False

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "time_sample",
                15,
                lambda: self.strings("_cfg_time_sample"),
                validator=loader.validators.Integer(minimum=1),
            ),
            loader.ConfigValue(
                "threshold",
                100,
                lambda: self.strings("_cfg_threshold"),
                validator=loader.validators.Integer(minimum=10),
            ),
            loader.ConfigValue(
                "local_floodwait",
                30,
                lambda: self.strings("_cfg_local_floodwait"),
                validator=loader.validators.Integer(minimum=10, maximum=3600),
            ),
            loader.ConfigValue(
                "forbidden_methods",
                ["joinChannel", "importChatInvite"],
                lambda: self.strings("_cfg_forbidden_methods"),
                validator=loader.validators.MultiChoice(
                    [
                        "sendReaction",
                        "joinChannel",
                        "importChatInvite",
                    ]
                ),
                on_change=lambda: self._client.forbid_constructors(
                    map(
                        lambda x: CONSTRUCTORS[x], self.config["forbidden_constructors"]
                    )
                ),
            ),
        )

    async def client_ready(self):
        asyncio.ensure_future(self._install_protection())

    async def _install_protection(self):
        await asyncio.sleep(30)  # Restart lock
        if hasattr(self._client._call, "_old_call_rewritten"):
            raise loader.SelfUnload("Already installed")

        old_call = self._client._call

        async def new_call(
            sender: "MTProtoSender",  # type: ignore
            request: "TLRequest",  # type: ignore
            ordered: bool = False,
            flood_sleep_threshold: int = None,
        ):
            await asyncio.sleep(random.randint(1, 5) / 100)
            if time.perf_counter() > self._suspend_until and not self.get(
                "disable_protection",
                True,
            ):
                request_name = type(request).__name__
                self._ratelimiter += [[request_name, time.perf_counter()]]

                self._ratelimiter = list(
                    filter(
                        lambda x: time.perf_counter() - x[1]
                        < int(self.config["time_sample"]),
                        self._ratelimiter,
                    )
                )

                if (
                    len(self._ratelimiter) > int(self.config["threshold"])
                    and not self._lock
                ):
                    self._lock = True
                    report = io.BytesIO(
                        json.dumps(
                            self._ratelimiter,
                            indent=4,
                        ).encode("utf-8")
                    )
                    report.name = "local_fw_report.json"

                    await self.inline.bot.send_document(
                        self.tg_id,
                        report,
                        caption=self.strings("warning").format(
                            self.config["local_floodwait"],
                            prefix=self.get_prefix(),
                        ),
                    )

                    # It is intented to use time.sleep instead of asyncio.sleep
                    time.sleep(int(self.config["local_floodwait"]))
                    self._lock = False

            return await old_call(sender, request, ordered, flood_sleep_threshold)

        self._client._call = new_call
        self._client._old_call_rewritten = old_call
        self._client._call._hikka_overwritten = True
        logger.debug("Successfully installed ratelimiter")

    async def on_unload(self):
        if hasattr(self._client, "_old_call_rewritten"):
            self._client._call = self._client._old_call_rewritten
            delattr(self._client, "_old_call_rewritten")
            logger.debug("Successfully uninstalled ratelimiter")

    @loader.command(
        ru_doc="<время в секундах> - Заморозить защиту API на N секунд",
        it_doc="<tempo in secondi> - Congela la protezione API per N secondi",
        de_doc="<Sekunden> - API-Schutz für N Sekunden einfrieren",
        tr_doc="<saniye> - API korumasını N saniye dondur",
        uz_doc="<soniya> - API himoyasini N soniya o'zgartirish",
        es_doc="<segundos> - Congela la protección de la API durante N segundos",
        kk_doc="<секунд> - API қорғауын N секундтік уақытта құлыптау",
    )
    async def suspend_api_protect(self, message: Message):
        """<time in seconds> - Suspend API Ratelimiter for n seconds"""
        args = utils.get_args_raw(message)

        if not args or not args.isdigit():
            await utils.answer(message, self.strings("args_invalid"))
            return

        self._suspend_until = time.perf_counter() + int(args)
        await utils.answer(message, self.strings("suspended_for").format(args))

    @loader.command(
        ru_doc="Включить/выключить защиту API",
        it_doc="Attiva/disattiva la protezione API",
        de_doc="API-Schutz einschalten / ausschalten",
        tr_doc="API korumasını aç / kapat",
        uz_doc="API himoyasini yoqish / o'chirish",
        es_doc="Activar / desactivar la protección de API",
        kk_doc="API қорғауын қосу / жою",
    )
    async def api_fw_protection(self, message: Message):
        """Toggle API Ratelimiter"""
        await self.inline.form(
            message=message,
            text=self.strings("u_sure"),
            reply_markup=[
                {"text": self.strings("btn_no"), "action": "close"},
                {"text": self.strings("btn_yes"), "callback": self._finish},
            ],
        )

    @property
    def _debugger(self) -> WebDebugger:
        return logging.getLogger().handlers[0].web_debugger

    async def _show_pin(self, call: InlineCall):
        await call.answer(f"Werkzeug PIN: {self._debugger.pin}", show_alert=True)

    @loader.command(
        ru_doc="Показать PIN Werkzeug",
        it_doc="Mostra il PIN Werkzeug",
        de_doc="PIN-Werkzeug anzeigen",
        tr_doc="PIN aracını göster",
        uz_doc="PIN vositasi ko'rsatish",
        es_doc="Mostrar herramienta PIN",
        kk_doc="PIN құралын көрсету",
    )
    async def debugger(self, message: Message):
        """Show the Werkzeug PIN"""
        await self.inline.form(
            message=message,
            text=self.strings("web_pin"),
            reply_markup=[
                [
                    {
                        "text": self.strings("web_pin_btn"),
                        "callback": self._show_pin,
                    }
                ],
                [
                    {"text": self.strings("proxied_url"), "url": self._debugger.url},
                    {
                        "text": self.strings("local_url"),
                        "url": f"http://127.0.0.1:{self._debugger.port}",
                    },
                ],
            ],
        )

    async def _finish(self, call: InlineCall):
        state = self.get("disable_protection", True)
        self.set("disable_protection", not state)
        await call.edit(self.strings("on" if state else "off"))
