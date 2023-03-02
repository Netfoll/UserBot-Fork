# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

import asyncio
import datetime
import io
import json
import logging
import time

from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import BotInlineCall

logger = logging.getLogger(__name__)


@loader.tds
class NetfollBackupMod(loader.Module):
    """Automatic database backup"""

    strings = {
        "name": "NetfollBackup",
        "period": (
            "⌚️ <b>Unit «ALPHA»</b> creates database backups periodically. You can"
            " change this behavior later.\n\nPlease, select the periodicity of"
            " automatic database backups"
        ),
        "saved": (
            "✅ Backup period saved. You can re-configure it later with"
            " .set_backup_period"
        ),
        "never": (
            "✅ I will not make automatic backups. You can re-configure it later with"
            " .set_backup_period"
        ),
        "invalid_args": (
            "🚫 <b>Specify correct backup period in hours, or `0` to disable</b>"
        ),
    }

    strings_ru = {
        "period": (
            "❗️<b>Советую включить функцию АвтоБэкапа</b> <i>(Unit Alpha)</i>"
            " <b><i>Время от времени Юнит будет создавать бэкапы вашего конфига, чтобы легко вернуть все данные в случае сбоя </i>\n"
            "В случае потери конфига разработчики никак не вернут ваши данные\n\n"
            "</b>‼️<b> Не с кем не делитесь файлами конфига, даже с разработчиками Netfoll! Они содержат конфиденциальные данные\n\n"
            "<i>Чтобы в ручную изменить время автобэкапа используйте </i></b><code>.autobackup\n\n"
            "</code>🔻 <b>Выберите срок Автобэкапа</b>"
        ),
        "saved": (
            "✅ Периодичность сохранена! Ее можно изменить с помощью .autobackup"
        ),
        "never": (
            "✅ Я не буду делать автоматические резервные копии. Можно отменить"
            " используя .autobackup"
        ),
        "invalid_args": (
            "🚫 <b>Укажи правильную периодичность в часах, или `0` для отключения</b>"
        ),
    }

    strings_ru = {
        "period": (
            "❗️<b>Раджу включити функцію Автобекапа</b> <i>(Unit Alpha)</i>"
            " <b><i>Час від часу Юніт буде створювати бекапи вашого конфіга, щоб легко повернути всі дані в разі збою </i>\n"
            "У разі втрати конфіга розробники ніяк не повернуть ваші дані\n\n"
            "</b>‼️<b> Ні з ким не діліться файлами конфігура, навіть з розробниками Netfol! Вони містять конфіденційні дані\n\n"
            "<i>Щоб вручну змінити час автобекапу використовуйте </i></b><code>.autobackup\n\n"
            "</code>🔻 <b>Виберіть термін Автобекапу</b>"
        ),
        "saved": (
            "✅ Періодичність збережена! Її можна змінити за допомогою .autobackup"
        ),
        "never": (
            "✅ Я не буду робити автоматичні резервні копії. Можна скасувати"
            " используя .autobackup"
        ),
        "invalid_args": (
            "🚫 <b>Вкажи правильну періодичність в годинах, або '0' для відключення</b>"
        ),
    }

    async def client_ready(self):
        if not self.get("period"):
            await self.inline.bot.send_photo(
                self.tg_id,
                photo="https://github.com/MXRRI/Netfoll/raw/stable/assets/BackUp.png",
                caption=self.strings("period"),
                reply_markup=self.inline.generate_markup(
                    utils.chunks(
                        [
                            {
                                "text": f"🕰 {i} h",
                                "callback": self._set_backup_period,
                                "args": (i,),
                            }
                            for i in [2, 12, 24]
                        ],
                        3,
                    )
                    + [
                        [
                            {
                                "text": "🚫 Never",
                                "callback": self._set_backup_period,
                                "args": (0,),
                            }
                        ]
                    ]
                ),
            )

        self._backup_channel, _ = await utils.asset_channel(
            self._client,
            "netfoll-backups",
            "📼 Your database backups will appear here",
            silent=True,
            archive=True,
            avatar="https://github.com/hikariatama/assets/raw/master/hikka-backups.png",
            _folder="hikka",
        )

        self.handler.start()

    async def _set_backup_period(self, call: BotInlineCall, value: int):
        if not value:
            self.set("period", "disabled")
            await call.answer(self.strings("never"), show_alert=True)
            await call.delete()
            return

        self.set("period", value * 60 * 60)
        self.set("last_backup", round(time.time()))

        await call.answer(self.strings("saved"), show_alert=True)
        await call.delete()

    @loader.command(
        ru_doc="<время в часах> - Установить частоту бэкапов",
        it_doc="<tempo in ore> - Imposta la frequenza dei backup",
        de_doc="<Stunden> - Setze die Backup-Frequenz",
        tr_doc="<saat cinsinden zaman> - Yedekleme periyodunu ayarla",
        uz_doc="<soatda vaqt> - E'lon tartibini belgilash",
        es_doc="<horas> - Establecer la frecuencia de copia de seguridad",
        kk_doc="<сағатты уақыт> - Резервтік көшірмелер қайдағы кезеңдерде жасалады",
    )
    async def autobackup(self, message: Message):
        """<time in hours> - Change backup frequency"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit() or int(args) not in range(200):
            await utils.answer(message, self.strings("invalid_args"))
            return

        if not int(args):
            self.set("period", "disabled")
            await utils.answer(message, f"<b>{self.strings('never')}</b>")
            return

        period = int(args) * 60 * 60
        self.set("period", period)
        self.set("last_backup", round(time.time()))
        await utils.answer(message, f"<b>{self.strings('saved')}</b>")

    @loader.loop(interval=1)
    async def handler(self):
        try:
            if self.get("period") == "disabled":
                raise loader.StopLoop

            if not self.get("period"):
                await asyncio.sleep(3)
                return

            if not self.get("last_backup"):
                self.set("last_backup", round(time.time()))
                await asyncio.sleep(self.get("period"))
                return

            await asyncio.sleep(
                self.get("last_backup") + self.get("period") - time.time()
            )

            backup = io.BytesIO(json.dumps(self._db).encode("utf-8"))
            backup.name = "netfoll-db-backup-{}.json".format(
                getattr(datetime, "datetime", datetime).now().strftime("%d-%m-%Y-%H-%M")
            )

            await self._client.send_file(self._backup_channel, backup)
            self.set("last_backup", round(time.time()))
        except loader.StopLoop:
            raise
        except Exception:
            logger.exception("NetfollBackup failed")
            await asyncio.sleep(60)
