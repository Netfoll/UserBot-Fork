# ©️ Hikka by Dan Gazizullin, 2021-2023
# ©️ Netfoll by Artur Bykov, 2022-20?? 
# This file is a part of Netfoll Userbot
# 🌐 https://github.com/MXRRI/Netfoll
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ---------------------------------------------------------------------------------
# ⠄⠄⠄⠄⡠⣿⢷⣻⣿⣾⣳⡇⢺⠟⠒⠒⠶⢤⣈⠃⢠⡀
# ⠄⠄⠄⢀⣼⡿⠋⢉⣉⣙⠿⠁⢁⣤⣤⣄⡀⠄⠈⠳⢾⣿⣄
# ⠄⠄⠄⢞⡞⠄⣴⣿⡿⠛⠓⠄⠉⠉⠉⠉⠹⣷⣄⠄⠄⠙⢿⣦
# ⠄⢀⣾⡟⠄⣸⠟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⢿⡀⠄⠰⣿⣆
# ⠄⢸⣿⠁⢸⣿⠄⠄⢸⢸⠄⠄⠄⢸⣆⢠⣀⡀⣧⣨⣻⡀⠄⢻⣿⣦⣀
# ⠄⢸⡇⡀⠘⣿⢰⣐⢾⢿⡀⠄⡀⢨⣎⣻⣷⣶⣿⣿⣿⣇⢀⢸⣿⣿⣿⣷
# ⠄⢸⣣⡇⣧⣿⣿⣿⣿⡎⢳⣟⠿⣿⣿⣏⣉⣿⣿⣿⢻⣿⣿⣾⣿⣿⣿⣿⣦
# ⠄⠄⢼⡇⢹⣿⡏⢠⣿⣿⠄⠉⠄⠄⠈⠄⢹⣿⠟⠼⢻⣿⣿⣿⣿⣿⣿⣿⣿
# ⠄⠄⠈⢿⢈⣿⡛⠘⣿⡇⠄⠄⡀⠄⠄⠄⠈⠉⠁⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿
# ⠄⠄⢀⣿⣼⡿⣿⣀⠄⠄⠄⠄⠃⠄⠄⠄⠄⠄⠄⠘⣻⡏⣿⣿⢻⣿⣿⣿⣿
# ⠄⠄⠾⢻⡇⣿⣸⣦⣀⠄⠄⠐⢟⠙⢻⠃⠄⠄⠄⣾⡏⣷⢻⡹⡟⣿⣿⡟⢿
# ⠄⢀⡴⢻⣇⢿⣷⢻⡟⠻⣶⣤⣀⠉⠄⣀⣴⡿⢣⡟⠄⣿⢸⡇⣰⡟⠻⠃⢸
# ⢠⡏⠄⠄⠈⠻⣿⣏⣷⠄⠈⠻⠉⠛⠛⠉⠄⠄⢛⠄⠄⠻⢠⠁⢛⠁⠄⠄⢸
# ⣼⠄⠄⠄⠄⠄⠈⢿⡘⠃⠄⠄⠄⠄⠄⠄⠠⠈⠄⠄⠄⢠⣸⣠⡞⠄⠄⠄⣿
# ⣤⠄⠄⠄⠄⠄⠄⢸⣇⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⣿⠟⠄⠄⠄⣸⣿
#
# 👾 Module for Telethon User Bot (Netfoll, Hikka, FTG)
# ---------------------------------------------------------------------------------
# meta developer: @netfoll
# meta description: Configurable ping

import datetime
import logging
import time

from telethon.tl.types import Message

from .. import loader, main, utils

logger = logging.getLogger(__name__)


class PingMod(loader.Module):

    strings = {
        "name": "Ping",
        "uptime": "👩‍💼 <b>Uptime</b>",
        "com": "{} <code>{}</code> <b>ms</b>\n{}",
        "modulesupports": "Модуль поддерживает значения {time} и {uptime}",
        "pingmsg": "Here you can configure custom response message"
    }

    strings_ru = {
        "name": "Ping",
        "uptime": "👩‍💼 <b>Аптайм</b>",
        "com": "{} <code>{}</code> <b>мс</b>\n{}",
        "modulesupports": "Модуль поддерживает значения {time} и {uptime}",
        "pingmsg": "Тут вы можете изменить ответное сообщения команды"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                "no",
                doc=lambda: self.strings("modulesupports"),
            ),
            loader.ConfigValue(
                "ping_message",
                "⏱ <b>Ping:</b>",
                lambda: self.strings("pingmsg"),
            ),
            loader.ConfigValue(
                "timezone",
                "0",
                lambda: "use 1, -1, -3 etc. to correct the server time on {time}",
            ),
        )

    def _render_ping(self):
        offset = datetime.timedelta(hours=self.config["timezone"])
        tz = datetime.timezone(offset)
        time2 = datetime.datetime.now(tz)
        time = time2.strftime("%H:%M:%S")
        uptime = utils.formatted_uptime()
        return (
            self.config["custom_message"].format(
                time=time,
                uptime=uptime,
            )
            if self.config["custom_message"] != "no"
            else (f'{self.strings("uptime")}: <b>{uptime}</b>')
        )

    @loader.command()
    async def ping(self, message: Message):
        """- Get your ping"""
        ping = self.config["ping_message"]
        start = time.perf_counter_ns()
        message = await utils.answer(message, "👾")
        try:
            await utils.answer(
                message,
                self.strings("com").format(
                    ping,
                    round((time.perf_counter_ns() - start) / 10**6, 3),
                    self._render_ping(),
                ),
            )
        except TypeError:
            await utils.answer(
                message,
                "Invalid number on .config -> Ping -> timezone, pls update it",
            )