# ---------------------------------------------------------------------------------
#  ,_     _          
#  |\_,-~/          
#  / _  _ |    ,--.  🌐 This module was loaded through https://t.me/hikkamods_bot
# (  @  @ )   / ,-'  🔓 Not licensed.
#  \  _T_/-._( (     
#  /         `. \    ⚠️ Owner of this bot doesn't take responsibility for any
# |         _  \ |   errors caused by this module or this module being non-working
#  \ \ ,  /      |   and doesn't take ownership of any copyrighted material.
#   || |-_\__   /    
#  ((_/`(____,-'     
# ---------------------------------------------------------------------------------
# Name: MyRep
# Description: Модуль с вашей репутацией
# Author: SekaiYoneya
# Commands:
# .rep | .myrep
# ---------------------------------------------------------------------------------

# @Sekai_Yoneya

from .. import loader, utils


@loader.tds
class MyRepMod(loader.Module):
    """Модуль с вашей репутацией"""

    strings = {"name": "Репутация"}

    async def client_ready(self, message, db):
        self.db = db
        self.db.set("MyRep", "repstatus", True)

    async def repcmd(self, message):
        """Включить режим репутаций."""
        repstatus = self.db.get("MyRep", "repstatus")
        if repstatus is not True:
            self.db.set("MyRep", "repstatus", True)
            await message.edit(f"<b>[MyRepMod] ✅Режим репутаций включен!</b>")
        else:
            self.db.set("MyRep", "repstatus", False)
            await message.edit(f"<b>[MyRepMod] ❌Режим репутаций выключен!</b>")

    async def myrepcmd(self, message):
        """Посмотреть свою репутацию. Используй: .myrep clear (очистка репутации)."""
        args = utils.get_args_raw(message)
        if args == "clear":
            self.db.set("MyRep", "my_repa", 0)
            return await message.edit("<b>[MyRepMod] 🔁Моя Репутация очищена.</b>")
        myrep = self.db.get("MyRep", "my_repa")
        repstatus = self.db.get("MyRep", "repstatus")
        if repstatus is not False:
            msg_repstatus = "[<i>✅Включен.</i>]"
        else:
            msg_repstatus = "[<i>❌Выключен.</i>]"
        await message.edit(
            f"♻️ <b>[</b><i>Репутация</i><b>]</b> ♻️\n<b>Статус режима: </b>{msg_repstatus}<b>\nКол-во: <i>{myrep}</i>.</b>"
        )

    async def watcher(self, message):
        try:
            number = self.db.get("MyRep", "my_repa", 0)
            repstatus = self.db.get("MyRep", "repstatus")
            if message.mentioned:
                if repstatus is not False:
                    if message.text == "+":
                        number += 1
                        self.db.set("MyRep", "my_repa", number)
                        await message.reply(
                            f"<b>Ты повысил мою репутацию!\nНовое значение: {number}.</b>"
                        )
                    if message.text == "+2":
                        number += 2
                        self.db.set("MyRep", "my_repa", number)
                        await message.reply(
                            f"<b>Ты повысил мою репутацию!\nНовое значение: {number}.</b>"
                        )
                    elif message.text == "-":
                        total = int(number) - 1
                        self.db.set("MyRep", "my_repa", total)
                        await message.reply(
                            f"<b>Ты понизил мою репутацию!\nНовое значение: {total}.</b>"
                        )
        except:
            pass