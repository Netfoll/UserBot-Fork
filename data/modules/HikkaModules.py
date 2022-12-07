# The MIT License (MIT)
# Copyright (c) 2022 penggrin, Morri

# meta developer: @penggrinmods
# scope: hikka_only
# scope: hikka_we

from .. import loader, utils
import logging


logger = logging.getLogger(__name__)


@loader.tds
class HikkaModulesMod(loader.Module):
    """List of all of the modules currently installed"""

    strings = {
        "name": "Net-Modules",
        "amount": "<emoji document_id=5210953824461662025>🎛</emoji> I have <b>{}</b> modules installed.\n",
        "modules": "<emoji document_id=5213347100498075719>💿</emoji> List:",
        "partial_load": (
            "\n\n<emoji document_id=5328239124933515868>⚙️</emoji> <b>it's not all modules"
            "Netfoll is loading</b>"
        ),
    }

    strings_ru = {
        "name": "Net-Модули",
        "amount": "<emoji document_id=5210953824461662025>🎛</emoji> У меня установлено <b>{}</b> модулей.\n",
        "modules": "<emoji document_id=5213347100498075719>💿</emoji> Список:\n",
        "partial_load": (
            "\n\n<emoji document_id=5328239124933515868>⚙️</emoji> <b>Это не все модули, "
            "Netfoll загружается</b>"
        ),
    }

    @loader.command(ru_doc="Показать все установленные модули")
    async def modscmd(self, message):
        """- List of all of the modules currently installed"""

        result = f"{self.strings('amount').format(str(len(self.allmodules.modules)))}\n{self.strings('modules')}"

        for mod in self.allmodules.modules:
            try:
                name = mod.strings["name"]
            except KeyError:
                name = mod.__clas__.__name__
            result += f"\n <emoji document_id=5213429323351990315>🛑</emoji> <code>{name}</code>"

        result += (
            ""
            if self.lookup("Loader")._fully_loaded
            else self.strings('partial_load')
        )

        await utils.answer(message, result)
        
