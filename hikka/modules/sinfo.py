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
        "names": "<emoji document_id=5172854840321114816>🔌</emoji> Info of System",
        "cpu": "<emoji document_id=5172869086727635492>💎</emoji> CPU",
        "core": "Cores",
        "ram": "<emoji document_id=5174693704799093859>📼</emoji> RAM",
        "use": "<emoji document_id=5174963725098025560>🧬</emoji> UserBot Usage",
        "pyver": "<emoji document_id=5172623642231571081>🪄</emoji> Python",
        "release": "<emoji document_id=5172814652312126185>💽</emoji> Release OS",
        "system": "<emoji document_id=5172622400986022463>💿</emoji> OS",
        "ver": "<emoji document_id=5174800460506202880>🎞</emoji> Kernel",
    }

    strings_ru = {
        "names": "<emoji document_id=5172854840321114816>🔌</emoji> Информация о системе",
        "core": "Ядер",
        "use": "<emoji document_id=5174963725098025560>🧬</emoji> ЮБ Использует",
        "release": "<emoji document_id=5172814652312126185>💽</emoji> Релиз ОС",
        "ver": "<emoji document_id=5174800460506202880>🎞</emoji> Ядро",
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
                f'<b>{self.strings("use")}: RAM {ram_use}MB / CPU{cpu_use}%</b>\n\n'
                f'<b>{self.strings("pyver")}: {pyver}</b>\n'
                f'<b>{self.strings("release")}: {release}</b>\n'
                f'<b>{self.strings("system")}: {system}</b>\n'
                f'<b>{self.strings("ver")}: {ver}</b>\n\n'
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