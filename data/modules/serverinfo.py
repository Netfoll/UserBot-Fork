__version__ = (2, 0, 0)

#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# Modified by Penggrin, Morri
# All credits goes to the original author

# meta pic: https://static.hikari.gay/serverinfo_icon.png
# meta banner: https://mods.hikariatama.ru/badges/serverinfo.jpg
# meta developer: @hikarimods
# requires: psutil
# scope: hikka_only
# scope: hikka_min 1.2.10

import contextlib
import os
import platform
import sys

import psutil
from telethon.tl.types import Message

from .. import loader, utils


def bytes_to_megabytes(b: int) -> int:
    return round(b / 1024 / 1024, 1)


@loader.tds
class serverInfoMod(loader.Module):
    """Show server info"""

    strings = {
        "name": "ServerInfo",
        "loading": (
            "<emoji document_id=5271897426117009417>🚘</emoji> <b>Loading server"
            " info...</b>"
        ),
        "servinfo": (
            "<emoji document_id=5213089234956590813>💽</emoji> <b>Server"
            " Info</b>:\n\n<emoji document_id=5210723648574335066>⚙️</emoji> <b>CPU:"
            " {cpu} Cores {cpu_load}%</b>\n<emoji"
            " document_id=5210727866232218958>🎚</emoji> <b>RAM: {ram} / {ram_load_mb}MB"
            " ({ram_load}%)</b>\n\n"
            "<emoji document_id=5211044070314484953>💿</emoji> <b>Kernel: {kernel}</b>\n{arch_emoji} <b>Arch: {arch}</b>\n<emoji"
            " document_id=5213347100498075719>💿</emoji> <b>OS: {os}</b>\n\n<emoji"
            " document_id=5211049786915955236>🤖</emoji> <b>Python: {python}</b>"
        ),
    }

    strings_ru = {
        "loading": (
            "<emoji document_id=5271897426117009417>🚘</emoji> <b>Загрузка информации о"
            " сервере...</b>"
        ),
        "servinfo": (
            "<emoji document_id=5213089234956590813>💽</emoji> <b>Информация о сервере"
            "</b>:\n\n<emoji document_id=5210723648574335066>⚙️</emoji> <b>CPU:"
            " {cpu} ядер(-ро) {cpu_load}%</b>\n<emoji"
            " document_id=5210727866232218958>🎚</emoji> <b>RAM: {ram} / {ram_load_mb}MB"
            " ({ram_load}%)</b>\n\n"
            "<emoji document_id=5211044070314484953>💿</emoji> <b>Kernel: {kernel}</b>\n{arch_emoji} <b>Arch: {arch}</b>\n<emoji"
            " document_id=5213347100498075719>💿</emoji> <b>OS: {os}</b>\n\n<emoji"
            " document_id=5211049786915955236>🤖</emoji> <b>Python: {python}</b>"
        ),
        "_cls_doc": "Показывает информацию о сервере",
    }

    @loader.command(ru_doc="Показать информацию о сервере")
    async def serverinfo(self, message: Message):
        """Show server info"""
        message = await utils.answer(message, self.strings("loading"))

        inf = {
            "cpu": "n/a",
            "cpu_load": "n/a",
            "ram": "n/a",
            "ram_load_mb": "n/a",
            "ram_load": "n/a",
            "kernel": "n/a",
            "arch_emoji": "n/a",
            "arch": "n/a",
            "os": "n/a",
        }

        with contextlib.suppress(Exception):
            inf["cpu"] = psutil.cpu_count(logical=True)

        with contextlib.suppress(Exception):
            inf["cpu_load"] = psutil.cpu_percent()

        with contextlib.suppress(Exception):
            inf["ram"] = bytes_to_megabytes(
                psutil.virtual_memory().total - psutil.virtual_memory().available
            )

        with contextlib.suppress(Exception):
            inf["ram_load_mb"] = bytes_to_megabytes(psutil.virtual_memory().total)

        with contextlib.suppress(Exception):
            inf["ram_load"] = psutil.virtual_memory().percent
            
        with contextlib.suppress(Exception):
            inf["kernel"] = platform.version()

        with contextlib.suppress(Exception):
            inf["arch"] = utils.escape_html(platform.architecture()[0])

        inf["arch_emoji"] = (
            "<emoji document_id=5211225489733068014>🎛</emoji>"
            if "64" in (inf.get("arch", "") or "")
            else "<emoji document_id=5211225489733068014>🎛</emoji>"
        )

        with contextlib.suppress(Exception):
            inf["os"] = utils.escape_html(f"{platform.system()} {platform.release()}")

        with contextlib.suppress(Exception):
            inf["python"] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        await utils.answer(message, self.strings("servinfo").format(**inf))
