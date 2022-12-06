# meta developer: @HikkaWE
# meta banner: https://0x0.st/ok_z.jpg

from .. import loader, utils
from telethon.tl.types import Message  # type: ignore
import random


@loader.tds
class StathamQuote(loader.Module):
    strings = {
        "name": "StathamQuote",
    }

    async def client_ready(self):
        self.messages = await self.client.get_messages("memstatham", limit=100)

    async def цитатаcmd(self, message: Message):
        """Лучшие цитаты Джейсона Стетхема на все века"""
        quote = random.choice(self.messages)
        await utils.answer(message, quote)
        if message.out:
            await message.delete()