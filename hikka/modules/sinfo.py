# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#
# ---------------------------------------------------------------------------------
#     ▀▄   ▄▀   👾 Module for Netfoll UserBot (based on Hikka 1.6.0)
#    ▄█▀███▀█▄  🔒 Licensed under the GNU GPLv3
#   █▀███████▀█ ⚠️ @DarkModules & @Netfoll
#   █ █▀▀▀▀▀█ █
#      ▀▀ ▀▀
# ---------------------------------------------------------------------------------
# Name: SysInfo
# Description: Show system info
# Author: Netfoll Team
# Commands:
# .sinfo
# ---------------------------------------------------------------------------------

# meta developer: @Netfoll
# scope: hikka_min 1.6.0
# requires: psutil

from .. import loader, utils
import platform
import psutil

__version__ = (1, 0, 0)


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
        "platform": "<emoji document_id=5370869711888194012>👾</emoji> Platform",
        "release": "<emoji document_id=5357204066550162638>🎛</emoji> Release OS",
        "system": "<emoji document_id=5357312566013993869>📼</emoji> OS",
        "distribution": "<emoji document_id=5357127263944975958>💽</emoji> Distribution:",
    }

    strings_ru = {
        "names": "<emoji document_id=5357506110125254467>💎</emoji> Информация о системе",
        "core": "Ядер",
        "use": "<emoji document_id=5357312566013993869>📼</emoji> ЮБ Использует",
        "platform": "<emoji document_id=5370869711888194012>👾</emoji> Плафторма",
        "release": "<emoji document_id=5357204066550162638>🎛</emoji> Релиз ОС",
        "distribution": "<emoji document_id=5357127263944975958>💽</emoji> Дистрибутив:",
    }

    strings_uk = {
        "names": "<emoji document_id=5357506110125254467>💎</emoji> Інформація про систему",
        "core": "Ядер",
        "use": "<emoji document_id=5357312566013993869>📼</emoji> ЮБ використовує",
        "platform": "<emoji document_id=5370869711888194012>👾</emoji> Платформа",
        "release": "<emoji document_id=5357204066550162638>🎛</emoji> Реліз ОС",
        "distribution": "<emoji document_id=5357127263944975958>💽</emoji> Дистрибутив:",
    }

    async def client_ready(self):
        if "Termux" in utils.get_named_platform():
            raise loader.SelfUnload   
    with open('/etc/os-release') as f:
        lines = f.readlines()            

    def info(self, message):
        names = self.strings("names")
        processor = utils.escape_html(platform.architecture()[0])
        ram = bytes_to_megabytes(psutil.virtual_memory().total - psutil.virtual_memory().available)
        ram_load_mb = bytes_to_megabytes(psutil.virtual_memory().total)
        ram_load_procent = psutil.virtual_memory().percent
        plat = utils.get_named_platform()
        with open('/etc/os-release') as f:
            lines = f.readlines()
        distribution = ""
        for line in lines:
            if line.startswith('PRETTY_NAME='):
                distribution = line.split('=')[1].strip().strip('"')
                break
        return (
            f"<b>{names}</b>\n"
            f'<b>{self.strings("platform")}: {plat}</b>\n\n'
            f'<b>{self.strings("cpu")} ({processor}): {psutil.cpu_count(logical=True)} {self.strings("core")} ({psutil.cpu_percent()}%)</b>\n'
            f'<b>{self.strings("ram")}: {ram}/{ram_load_mb} MB ({ram_load_procent}%)</b>\n'
            f'<b>{self.strings("use")}: {utils.get_ram_usage()} MB / CPU {utils.get_cpu_usage()}%</b>\n\n'
            f'<b>{self.strings("pyver")}: {platform.python_version()}</b>\n'
            f'<b>{self.strings("release")}: {platform.version()}</b>\n'
            f'<b>{self.strings("system")}: {platform.system()} ({platform.release()})</b>\n'
            f'<b>{self.strings("distribution")}: {distribution}</b>\n'
        )

    @loader.command(ru_doc="Показать информацию о системе")
    async def sinfocmd(self, message):
        """Show System"""
        await utils.answer(message, self.info(message))
