# ▒█░▒█ ▒█▀▀▀ ▒█▀▀█ ░█▀▀█
# ▒█▀▀█ ▒█▀▀▀ ▒█░▄▄ ▒█▄▄█
# ▒█░▒█ ▒█▄▄▄ ▒█▄▄█ ▒█░▒█

# Licensed under the GNU AGPLv3
# https://www.gnu.org/licenses/agpl-3.0.html
# Name: HegaCode
# Description: Python code
# Author: https://t.me/hegakura

# Modified by Penggrin, Morri
# All credits goes to the original author

# scope: hikka_only
# scope: hikka_we

from .. import loader, main, utils

from telethon.tl.types import Message
from io import StringIO
from meval import meval
from types import ModuleType

import telethon
import sys
import itertools
import traceback
import typing
import logging

logger = logging.getLogger(__name__)


@loader.tds
class HikkaHegaCode(loader.Module):
    """Runs Python code"""
    strings = {
        "name": "HikkaHegaCode",
        "code": "Code",
        "result": "Result",
    }

    strings_ru = {
        "code": "Код",
        "result": "Результат",
    }

    def get_sub(self, obj: typing.Any, _depth: int = 1) -> dict:
        """Get all callable capitalised objects in an object recursively, ignoring _*"""
        return {
            **dict(
                filter(
                    lambda x: x[0][0] != "_"
                    and x[0][0].upper() == x[0][0]
                    and callable(x[1]),
                    obj.__dict__.items(),
                )
            ),
            **dict(
                itertools.chain.from_iterable(
                    [
                        self.get_sub(y[1], _depth + 1).items()
                        for y in filter(
                            lambda x: x[0][0] != "_"
                            and isinstance(x[1], ModuleType)
                            and x[1] != obj
                            and x[1].__package__.rsplit(".", _depth)[0]
                            == "telethon.tl",
                            obj.__dict__.items(),
                        )
                    ]
                )
            ),
        }

    async def getattrs(self, message: Message) -> dict:
        reply = await message.get_reply_message()
        return {
            **{
                "message": message,
                "client": self._client,
                "_client": self._client,
                "reply": reply,
                "r": reply,
                **self.get_sub(telethon.tl.types),
                **self.get_sub(telethon.tl.functions),
                "event": message,
                "chat": message.to_id,
                "telethon": telethon,
                "utils": utils,
                "main": main,
                "loader": loader,
                "f": telethon.tl.functions,
                "c": self._client,
                "m": message,
                "lookup": self.lookup,
                "self": self,
                "db": self.db,
            },
        }

    @loader.command(ru_doc="Алиас для .e")
    async def evalcmd(self, message: Message):
        """Alias for .e"""
        await self.ecmd(message)

    @loader.command(ru_doc="Алиас для .e")
    async def pcmd(self, message: Message):
        """Alias for .e"""
        await self.ecmd(message)

    @loader.command(ru_doc="<code> - Выполняет Python код")
    async def ecmd(self, message: Message):
        """<code> - Run Python code"""
        code = utils.get_args_raw(message)
        logs = ''
        old_stdout = sys.stdout
        result = sys.stdout = StringIO()

        try:
            await meval(
                code,
                globals(),
                **await self.getattrs(message),
            )
        except Exception:
            logs = traceback.format_exc(0)

        sys.stdout = old_stdout

        if logs:
            await utils.answer(
                message,
                f"<emoji document_id=5420315771991497307>🔥</emoji> <b>{self.strings('code')}:</b>\n<code>{code}</code>\n"
                f"\n<emoji document_id=5472146462362048818>💡</emoji> <b>{self.strings('result')}:</b>\n<code>{logs}</code>"
            )
        else:
            try:
                await utils.answer(
                    message,
                    f"<emoji document_id=5420315771991497307>🔥</emoji> <b>{self.strings('code')}:</b>\n<code>{code}</code>\n"
                    f"\n<emoji document_id=5472146462362048818>💡</emoji> <b>{self.strings('result')}:</b>\n<code>{result.getvalue()}</code>"
                )
            except Exception:
                await utils.answer(
                    message,
                    f"<emoji document_id=5420315771991497307>🔥</emoji> <b>{self.strings('code')}:</b>\n<code>{code}</code>\n"
                    f"\n<emoji document_id=5472146462362048818>💡</emoji> <b>{self.strings('result')}:</b>\n<code>400 MESSAGE_TOO_LONG</code>"
                )
