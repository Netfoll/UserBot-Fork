#
# 🔒 The MIT License (MIT)
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#
# ---------------------------------------------------------------------------------
#     ▀▄   ▄▀   👾 Module for Netfoll User Bot (based on Hikka 1.6.0)
#    ▄█▀███▀█▄  🔒 The MIT License (MIT)
#   █▀███████▀█ ⚠️ Owner @DarkModules and @Netfoll
#   █ █▀▀▀▀▀█ █
#      ▀▀ ▀▀
# ---------------------------------------------------------------------------------
# meta developer: @Netfoll
# scope: hikka_min 1.6.0

from .. import loader, utils
import logging


logger = logging.getLogger(__name__)


@loader.tds
class ModsMod(loader.Module):
    """List of all of the modules currently installed"""

    strings = {
        "name": "Mods",
        "amount": "<emoji document_id=5316573023094971227>📦</emoji> Right now there is <b>{}</b> modules loaded:\n",
        "partial_load": (
            "\n<emoji document_id=5328239124933515868>⚙️</emoji> <b>it's not all modules"
            " Netfoll is loading</b>"
        ),
        "cmd": "<emoji document_id=546974131930996757> 💫 </emoji> <i><b>To find out the module commands, use <code>{}help</code></i></b>\n",
        "module": "<emoji document_id=5402093879316982515>✨</emoji>",
        "core_module": "<emoji document_id=5400245067694747959>💫</emoji>",
    }

    strings_ru = {
        "amount": "<emoji document_id=5316573023094971227>📦</emoji> Сейчас загружено <b>{}</b> модулей:",
        "partial_load": (
            "\n<emoji document_id=5328239124933515868>⚙️</emoji> <b>Это не все модули,"
            " Netfoll загружается</b>"
        ),
        "cmd": "<emoji document_id=5469741319330996757>💫</emoji> <i><b>Чтобы узнать команды модуля используй <code>{}help</code></i></b>\n",
    }

    strings_uk = {
        "amount": "<emoji document_id=5316573023094971227>📦</emoji> Зараз завантажено <b>{}</b> модулей:",
        "partial_load": (
            "\n<emoji document_id=5328239124933515868>⚙️</emoji> <b>Це не всі модулі,"
            " Netfoll завантажувати</b>"
        ),
        "cmd": "<emoji document_id=5469741319330996757>💫</emoji> <i><b>Щоб дізнатися команди модуля використовуй <code>{}help</code></i></b>\n",
    }

    @loader.command(
        ru_doc="Показать все установленные модули",
        ua_doc="Показати всі встановлені модулі",
    )
    async def modscmd(self, message):
        """- List of all of the modules currently installed"""

        prefix = f"{self.strings('cmd').format(str(self.get_prefix()))}\n"
        result = f"{self.strings('amount').format(str(len(self.allmodules.modules)))}\n"

        for mod in self.allmodules.modules:
            try:
                name = mod.strings["name"]
            except KeyError:
                name = mod.__clas__.__name__
            emoji = (
                self.strings("core_module")
                if mod.__origin__.startswith("<core")
                else self.strings("module")
            )
            result += f"\n {emoji} <code>{name}</code>"

        result += (
            ""
            if self.lookup("Loader").fully_loaded
            else f"\n\n{self.strings('partial_load')}"
        )
        result += f"\n\n {prefix}"

        await utils.answer(message, result)
