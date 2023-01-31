# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 
# ---------------------------------------------------------------------------------
#     ▀▄   ▄▀   👾 Module for Netfoll User Bot (based on Hikka 1.6.0)
#    ▄█▀███▀█▄  🔒 Licensed under the GNU GPLv3
#   █▀███████▀█ ⚠️ Owner @DarkModules and @Netfoll
#   █ █▀▀▀▀▀█ █
#      ▀▀ ▀▀
# ---------------------------------------------------------------------------------
# Name: SysImfo
# Description: Show System
# Author: Netfoll
# Commands:
# .sinfo
# ---------------------------------------------------------------------------------

from telethon.tl.types import Message

from .. import loader, utils
import platform
import psutil

__version__ = (1, 0, 0)
# meta developer: @Netfoll
# scope: hikka_min 1.6.0
# requires: psutil

def bytes_to_megabytes(b: int) -> int:
    return round(b / 1024 / 1024, 1)

@loader.tds
class SysInfoMod(loader.Module):
    """Simple System Info for Netfoll UserBot (And Hikka Support)"""

    strings = {
        "name": "SysInfo",
        "names": "<emoji document_id=5357506110125254467>💎</emoji> Info of System",
        "cpu": "<emoji document_id=5357123346934802012>🚀</emoji> CPU",
        "core": "Cores",
        "ram": "<emoji document_id=5357488530824112765>⚙️</emoji> RAM",
        "use": "<emoji document_id=5357312566013993869>📼</emoji> UserBot Usage",
        "pyver": "<emoji document_id=5357560458641416842>🤖</emoji> Python",
        "release": "<emoji document_id=5357204066550162638>🎛</emoji> Release OS",
        "system": "<emoji document_id=5357312566013993869>📼</emoji> OS",
    }

    strings_ru = {
        "names": "<emoji document_id=5357506110125254467>💎</emoji> Информация о системе",
        "core": "Ядер",
        "use": "<emoji document_id=5357312566013993869>📼</emoji> ЮБ Использует",
        "release": "<emoji document_id=5357204066550162638>🎛</emoji> Релиз ОС",
    }

    def info(self, message):
        names = self.strings("names")
        processor = utils.escape_html(platform.architecture()[0])
        pyver = platform.python_version()
        ver = platform.release()
        system = platform.system()
        release = platform.version()
        cores = psutil.cpu_count(logical=True)
        cpu_load = psutil.cpu_percent()
        ram = bytes_to_megabytes(psutil.virtual_memory().total - psutil.virtual_memory().available)
        ram_load_mb = bytes_to_megabytes(psutil.virtual_memory().total)
        ram_load_procent = psutil.virtual_memory().percent
        cpu_use = utils.get_cpu_usage()
        ram_use = utils.get_ram_usage()
        
        return (
                f"<b>{names}</b>\n\n"
                f'<b>{self.strings("cpu")} ({processor}): {cores} {self.strings("core")} ({cpu_load}%)</b>\n'
                f'<b>{self.strings("ram")}: {ram}/{ram_load_mb} MB ({ram_load_procent}%)</b>\n'
                f'<b>{self.strings("use")}: {ram_use} MB / CPU{cpu_use}%</b>\n\n'
                f'<b>{self.strings("pyver")}: {pyver}</b>\n'
                f'<b>{self.strings("release")}: {release}</b>\n'
                f'<b>{self.strings("system")}: {system} ({ver})</b>\n\n'
            )
    @loader.command(
    ru_doc="Показать информацию о системе"
    )
    async def sinfocmd(self, message):
        """Show System"""       
        await utils.answer(
                message,
                self.info(message),
            )