# meta developer: @HikkaWE
# meta banner: https://0x0.st/okfZ.jpg

from .. import loader, utils
from telethon.tl.types import Message  # type: ignore
import random


@loader.tds
class RyanGosling(loader.Module):
    strings = {
        "name": "RyanGosling",
    }

    async def client_ready(self):
        self.messages = await self.client.get_messages("gooslya_mem", limit=100)

    async def гослингcmd(self, message: Message):
        """Скинуть гослинга"""
        RyanGosling = random.choice(self.messages)
        await utils.answer(message, RyanGosling)
        if message.out:
            await message.delete()