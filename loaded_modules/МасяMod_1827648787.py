# Name: Масюнчик
# Description: Масюнчик на все случаи жизни
# Author: Morri
# Commands:
# .мася
# ---------------------------------------------------------------------------------

# meta developer: @HikkaWE
# scope: hikka_only
# scope: hikka_min 1.3.0

import random
from telethon.tl.types import Message
from .. import loader


@loader.tds
class МасяMod(loader.Module):
    """Масюнчик на все случаи жизни"""

    strings = {"name": "Масюнчик"}

    @loader.command()
    async def масяcmd(self, message: Message):
        """--> масюнчик"""
        reply = await message.get_reply_message()
        m = random.choice(await self.client.get_messages("@MASYASTICK", limit=100))
        if reply:
            await self.client.send_message(message.chat_id, file=m, reply_to=reply)
        else:
            await message.respond(file=m)

        if message.out:
            await message.delete()