#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# Modified by Penggrin, Morri
# All credits goes to the original author

# scope: hikka_we

import asyncio
import atexit
import contextlib
import logging
import sys
import time
import typing

from telethon.tl.functions.messages import (
    GetDialogFiltersRequest,
    UpdateDialogFilterRequest,
)
from telethon.tl.types import DialogFilter, Message
from telethon.extensions.html import CUSTOM_EMOJIS

from .. import loader, utils, main

from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds
class HikkaRestartMod(loader.Module):
    """Restarts Hikka WE"""

    strings = {
        "name": "HikkaRestart",
        "source": (
            "<emoji document_id=5456255401194429832>📖</emoji> <b>Read the source code"
            " from</b> <a href='{}'>here</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>🕗</emoji> <b>Your {} is"
            " restarting...</b>"
        ),
        "success": (
            "<emoji document_id=6321050180095313397>⏱</emoji> <b>Restart successful!"
            " {}</b>\n<i>But still loading modules...</i>\n<i>Restart took {}s</i>"
        ),
        "btn_restart": "🔄 Restart",
        "restart_confirm": "❓ <b>Are you sure you want to restart?</b>",
        "secure_boot_confirm": (
            "❓ <b>Are you sure you want to restart in secure boot mode?</b>"
        ),
        "cancel": "🚫 Cancel",
        "full_success": (
            "<emoji document_id=6323332130579416910>👍</emoji> <b>Userbot is fully"
            " loaded! {}</b>\n<i>Full restart took {}s</i>"
        ),
        "secure_boot_complete": (
            "🔒 <b>Secure boot completed! {}</b>\n<i>Restart took {}s</i>"
        ),
    }

    strings_ru = {
        "source": (
            "<emoji document_id=5456255401194429832>📖</emoji> <b>Исходный код можно"
            " прочитать</b> <a href='{}'>здесь</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>🕗</emoji> <b>Твоя {}"
            " перезагружается...</b>"
        ),
        "success": (
            "<emoji document_id=6321050180095313397>⏱</emoji> <b>Перезагрузка"
            " успешна! {}</b>\n<i>Но модули еще загружаются...</i>\n<i>Перезагрузка"
            " заняла {} сек</i>"
        ),
        "full_success": (
            "<emoji document_id=6323332130579416910>👍</emoji> <b>Юзербот полностью"
            " загружен! {}</b>\n<i>Полная перезагрузка заняла {} сек</i>"
        ),
        "secure_boot_complete": (
            "🔒 <b>Безопасная загрузка завершена! {}</b>\n<i>Перезагрузка заняла {}"
            " сек</i>"
        ),
        "btn_restart": "🔄 Перезагрузиться",
        "restart_confirm": "❓ <b>Ты уверен, что хочешь перезагрузиться?</b>",
        "secure_boot_confirm": (
            "❓ <b>Ты уверен, что"
            " хочешь перезагрузиться в режиме безопасной загрузки?</b>"
        ),
        "cancel": "🚫 Отмена",
        "_cls_doc": "Перезапускает Hikka WE",
    }

    async def update_complete(self):
        logger.debug("Restart successful! Edit message")
        start = self.get("restart_ts")
        try:
            took = round(time.time() - start)
        except Exception:
            took = "N/A"

        msg = self.strings("success").format(utils.ascii_face(), took)
        ms = self.get("selfupdatemsg")

        if ":" in str(ms):
            chat_id, message_id = ms.split(":")
            chat_id, message_id = int(chat_id), int(message_id)
            await self._client.edit_message(chat_id, message_id, msg)
            return

        await self.inline.bot.edit_message_text(
            inline_message_id=ms,
            text=self.inline.sanitise_text(msg),
        )

    @loader.owner
    @loader.command(
        ru_doc="Перезагружает юзербот",
        de_doc="Startet den Userbot neu",
        tr_doc="Kullanıcı botunu yeniden başlatır",
        uz_doc="Foydalanuvchi botini qayta ishga tushiradi",
        hi_doc="उपयोगकर्ता बॉट को रीस्टार्ट करता है",
        ja_doc="ユーザーボットを再起動します",
        kr_doc="사용자 봇을 다시 시작합니다",
        ar_doc="يعيد تشغيل البوت",
        es_doc="Reinicia el bot",
    )
    async def restart(self, message: Message):
        """Restarts the userbot"""
        secure_boot = "--secure-boot" in utils.get_args_raw(message)
        try:
            if (
                "--force" in (utils.get_args_raw(message) or "")
                or "-f" in (utils.get_args_raw(message) or "")
                or not self.inline.init_complete
                or not await self.inline.form(
                    message=message,
                    text=self.strings(
                        "secure_boot_confirm" if secure_boot else "restart_confirm"
                    ),
                    reply_markup=[
                        {
                            "text": self.strings("btn_restart"),
                            "callback": self.inline_restart,
                            "args": (secure_boot,),
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                )
            ):
                raise
        except Exception:
            await self.restart_common(message, secure_boot)

    async def inline_restart(self, call: InlineCall, secure_boot: bool = False):
        await self.restart_common(call, secure_boot=secure_boot)

    async def process_restart_message(self, msg_obj: typing.Union[InlineCall, Message]):
        self.set(
            "selfupdatemsg",
            msg_obj.inline_message_id
            if hasattr(msg_obj, "inline_message_id")
            else f"{utils.get_chat_id(msg_obj)}:{msg_obj.id}",
        )

    async def restart_common(
        self,
        msg_obj: typing.Union[InlineCall, Message],
        secure_boot: bool = False,
    ):
        if (
            hasattr(msg_obj, "form")
            and isinstance(msg_obj.form, dict)
            and "uid" in msg_obj.form
            and msg_obj.form["uid"] in self.inline._units
            and "message" in self.inline._units[msg_obj.form["uid"]]
        ):
            message = self.inline._units[msg_obj.form["uid"]]["message"]
        else:
            message = msg_obj

        if secure_boot:
            self._db.set(loader.__name__, "secure_boot", True)

        msg_obj = await utils.answer(
            msg_obj,
            self.strings("restarting_caption").format(
                utils.get_platform_emoji(self._client)
                if self._client.hikka_me.premium
                and CUSTOM_EMOJIS
                and isinstance(msg_obj, Message)
                else "Hikka"
            )
        )

        await self.process_restart_message(msg_obj)

        self.set("restart_ts", time.time())

        await self._db.remote_force_save()

        with contextlib.suppress(Exception):
            await main.hikka.web.stop()

        atexit.register(restart, *sys.argv[1:])
        handler = logging.getLogger().handlers[0]
        handler.setLevel(logging.CRITICAL)

        for client in self.allclients:
            # Terminate main loop of all running clients
            # Won't work if not all clients are ready
            if client is not message.client:
                await client.disconnect()

        await message.client.disconnect()
        sys.exit(0)

    @loader.unrestricted
    @loader.command(
        ru_doc="Показать ссылку на исходный код проекта",
        de_doc="Zeigt den Link zum Quellcode des Projekts an",
        tr_doc="Proje kaynak kodu bağlantısını gösterir",
        uz_doc="Loyihaning manba kodiga havola ko'rsatadi",
        hi_doc="प्रोजेक्ट कोड का लिंक दिखाएं",
        ja_doc="プロジェクトのソースコードへのリンクを表示します",
        kr_doc="프로젝트 소스 코드 링크를 표시합니다",
        ar_doc="يعرض رابط مصدر البوت",
        es_doc="Muestra el enlace al código fuente del proyecto",
    )
    async def source(self, message: Message):
        """Links the source code of this project"""
        await utils.answer(
            message,
            self.strings("source").format("https://t.me/HikkaWE/3"),
        )

    async def client_ready(self):
        if self.get("selfupdatemsg") is not None:
            try:
                await self.update_complete()
            except Exception:
                logger.exception("Failed to complete update!")

        if self.get("do_not_create", False):
            return

        try:
            await self._add_folder()
        except Exception:
            logger.exception("Failed to add folder!")
        finally:
            self.set("do_not_create", True)

    async def _add_folder(self):
        folders = await self._client(GetDialogFiltersRequest())

        if any(getattr(folder, "title", None) == "hikka" for folder in folders):
            return

        try:
            folder_id = (
                max(
                    folders,
                    key=lambda x: x.id,
                ).id
                + 1
            )
        except ValueError:
            folder_id = 2

        try:
            await self._client(
                UpdateDialogFilterRequest(
                    folder_id,
                    DialogFilter(
                        folder_id,
                        title="hikka",
                        pinned_peers=(
                            [
                                await self._client.get_input_entity(
                                    self._client.loader.inline.bot_id
                                )
                            ]
                            if self._client.loader.inline.init_complete
                            else []
                        ),
                        include_peers=[
                            await self._client.get_input_entity(dialog.entity)
                            async for dialog in self._client.iter_dialogs(
                                None,
                                ignore_migrated=True,
                            )
                            if dialog.name
                            in {
                                "hikka-logs",
                                "hikka-onload",
                                "hikka-assets",
                                "hikka-backups",
                                "hikka-acc-switcher",
                                "silent-tags",
                            }
                            and dialog.is_channel
                            and (
                                dialog.entity.participants_count == 1
                                or dialog.entity.participants_count == 2
                                and dialog.name in {"hikka-logs", "silent-tags"}
                            )
                            or (
                                self._client.loader.inline.init_complete
                                and dialog.entity.id
                                == self._client.loader.inline.bot_id
                            )
                            or dialog.entity.id
                            in [
                                1554874075,
                                1697279580,
                                1679998924,
                            ]  # official hikka chats
                        ],
                        emoticon="🐱",
                        exclude_peers=[],
                        contacts=False,
                        non_contacts=False,
                        groups=False,
                        broadcasts=False,
                        bots=False,
                        exclude_muted=False,
                        exclude_read=False,
                        exclude_archived=False,
                    ),
                )
            )
        except Exception:
            logger.critical(
                "Can't create Hikka folder. Possible reasons are:\n"
                "- User reached the limit of folders in Telegram\n"
                "- User got floodwait\n"
                "Ignoring error and adding folder addition to ignore list"
            )

    async def full_restart_complete(self, secure_boot: bool = False):
        start = self.get("restart_ts")

        try:
            took = round(time.time() - start)
        except Exception:
            took = "n/a"

        self.set("restart_ts", None)

        ms = self.get("selfupdatemsg")
        msg = self.strings(
            "secure_boot_complete" if secure_boot else "full_success"
        ).format(utils.ascii_face(), took)

        if ms is None:
            return

        self.set("selfupdatemsg", None)

        if ":" in str(ms):
            chat_id, message_id = ms.split(":")
            chat_id, message_id = int(chat_id), int(message_id)
            await self._client.edit_message(chat_id, message_id, msg)
            await asyncio.sleep(60)
            await self._client.delete_messages(chat_id, message_id)
            return

        await self.inline.bot.edit_message_text(
            inline_message_id=ms,
            text=self.inline.sanitise_text(msg),
        )


def restart(*argv):
    # .bat will do the rest
    sys.exit(0)
