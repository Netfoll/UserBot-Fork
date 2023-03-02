# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

import asyncio
import contextlib
import logging
import os
import subprocess
import sys
import time
import typing

import git
from git import GitCommandError, Repo
from telethon.extensions.html import CUSTOM_EMOJIS
from telethon.tl.functions.messages import (
    GetDialogFiltersRequest,
    UpdateDialogFilterRequest,
)
from telethon.tl.types import DialogFilter, Message

from .. import loader, main, utils, version
from .._internal import restart
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds
class UpdaterMod(loader.Module):
    """Updates itself"""

    strings = {
        "name": "Updater",
        "source": (
            "<emoji document_id=5456255401194429832>📖</emoji> <b>Read the source code"
            " from</b> <a href='{}'>here</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=5325792861885570739>🕗</emoji> <b>Your {} is"
            " restarting...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>🕗</emoji> <b>Downloading"
            " updates...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>🕗</emoji> <b>Installing"
            " updates...</b>"
        ),
        "success": (
            "<emoji document_id=5305683825005700455>🕗</emoji> <b>Restart successful!"
            " {}</b>\n<i>Loading modules...</i>\n<i>Restart took {}s</i>"
        ),
        "origin_cfg_doc": "Git origin URL, for where to update from",
        "btn_restart": "🔄 Restart",
        "btn_update": "🧭 Update",
        "restart_confirm": "❓ <b>Are you sure you want to restart?</b>",
        "secure_boot_confirm": (
            "❓ <b>Are you sure you want to restart in secure boot mode?</b>"
        ),
        "update_confirm": (
            "❓ <b>Are you sure you"
            " want to update?\n\n<a"
            ' href="https://github.com/MXRRI/Netfoll/{}">{}</a> ⤑ <a'
            ' href="https://github.com/MXRRI/Netfoll/{}">{}</a></b>'
        ),
        "no_update": "🚸 <b>You are on the latest version, pull updates anyway?</b>",
        "cancel": "🚫 Cancel",
        "lumihost_restart": (
            "<b>Your {} is"
            " restarting...</b>"
        ),
        "lumihost_update": (
            "<b>Your {} is"
            " updating...</b>"
        ),
        "full_success": (
            "<emoji document_id=5348526883992510786>💜</emoji> <b>Userbot ready"
            " to use! {}</b>\n<i>Full restart took {}s</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>🔐</emoji> <b>Secure boot completed!"
            " {}</b>\n<i>Restart took {}s</i>"
        ),
    }

    strings_ru = {
        "source": (
            "<emoji document_id=5456255401194429832>📖</emoji> <b>Исходный код можно"
            " прочитать</b> <a href='{}'>здесь</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=5325792861885570739>🕗</emoji> <b>Твой {}"
            " перезагружается...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>🕗</emoji> <b>Скачивание"
            " обновлений...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>🕗</emoji> <b>Установка"
            " обновлений...</b>"
        ),
        "success": (
            "<emoji document_id=5305683825005700455>🕗</emoji> <b>Перезагрузка"
            " успешна! {}</b>\n<i>Идет процесс загрузки модулей...</i>\n<i>Перезагрузка"
            " длилась {} сек</i>"
        ),
        "full_success": (
            "<emoji document_id=5348526883992510786>💜</emoji> <b>Юзербот готов к"
            " работе! {}</b>\n<i>Полная перезагрузка заняла {} сек</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>🔐</emoji> <b>Безопасная загрузка"
            " завершена! {}</b>\n<i>Перезагрузка заняла {} сек</i>"
        ),
        "origin_cfg_doc": "Ссылка, из которой будут загружаться обновления",
        "btn_restart": "🔄 Перезагрузиться",
        "btn_update": "🧭 Обновиться",
        "restart_confirm": "❓ <b>Ты уверен, что хочешь перезагрузиться?</b>",
        "secure_boot_confirm": (
            "❓ <b>Ты уверен, что"
            " хочешь перезагрузиться в режиме безопасной загрузки?</b>"
        ),
        "update_confirm": (
            "❓ <b>Ты уверен, что"
            " хочешь обновиться??\n\n<a"
            ' href="https://github.com/MXRRI/Netfoll/commit/{}">{}</a> ⤑ <a'
            ' href="https://github.com/MXRRI/Netfoll/commit/{}">{}</a></b>'
        ),
        "no_update": "🚸 <b>У тебя последняя версия. Обновиться принудительно?</b>",
        "cancel": "🚫 Отмена",
        "_cls_doc": "Обновляет юзербот",
        "lumihost_restart": (
            "<b>Твой {}"
            " перезагружается...</b>"
        ),
        "lumihost_update": (
            "<b>Твой {}"
            " обновляется...</b>"
        ),
    }

    strings_uk = {
        "source": (
            "<emoji document_id=5456255401194429832>📖</emoji> <b>Вихідний код можна"
            " прочитавши</b> <a href='{}'>тут</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=5325792861885570739>🕗</emoji> <b>Твого {}"
            " перезавантажувати...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>🕗</emoji> <b>Скачування"
            " оновлення...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>🕗</emoji> <b>Установка"
            " оновлення...</b>"
        ),
        "success": (
            "<emoji document_id=5305683825005700455>🕗</emoji> <b>Перезавантаження"
            " успішний! {}</b>\n<i>Йде процес завантаження Модулів...</i>\n<i>Перезавантаження"
            " тривати {} сек</i>"
        ),
        "full_success": (
            "<emoji document_id=5348526883992510786>💜</emoji> <b>Юзербот готовий до"
            " роботи! {}</b>\n<i>Повне перезавантаження зайняло {} сек</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>🔐</emoji> <b>Безпечне завантаження"
            " завершений! {}</b>\n<i>Перезавантаження зайняло {} сек</i>"
        ),
        "origin_cfg_doc": "Посилання, з якої будуть завантажуватися оновлення",
        "btn_restart": "🔄 Перезавантажитися",
        "btn_update": "🧭 Оновитися",
        "restart_confirm": "❓ <b>Ви впевнені, що хочете перезавантажитися?</b>",
        "secure_boot_confirm": (
            "❓ <b>Ти впевнений, що"
            " хочеш перезавантажитися в режимі безпечного завантаження?</b>"
        ),
        "update_confirm": (
            "❓ <b>Ти впевнений, що"
            " хочеш оновитися??\n\n<a"
            ' href="https://github.com/MXRRI/Netfoll/commit/{}">{}</a> ⤑ <a'
            ' href="https://github.com/MXRRI/Netfoll/commit/{}">{}</a></b>'
        ),
        "no_update": "🚸 <b>У вас остання версія. Оновитися примусово?</b>",
        "cancel": "🚫 Скасування",
        "_cls_doc": "Оновлює юзербот",
        "lumihost_restart": (
            "<b>Твого {}"
            " перезавантажувати...</b>"
        ),
        "lumihost_update": (
            "<b>Твого {}"
            " оновлюватися...</b>"
        ),
    }    

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "GIT_ORIGIN_URL",
                "https://github.com/MXRRI/Netfoll",
                lambda: self.strings("origin_cfg_doc"),
                validator=loader.validators.Link(),
            )
        )

    @loader.owner
    @loader.command(ru_doc="Перезагружает юзербот")
    async def restart(self, message: Message):
        """Restarts the userbot"""
        args = utils.get_args_raw(message)
        secure_boot = any(trigger in args for trigger in {"--secure-boot", "-sb"})
        try:
            if (
                "-f" in args
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
                else "<emoji document_id=5364105417569868801>😎</emoji> <b>LumiHost</b>"
            )
            if "LUMIHOST" not in os.environ
            else self.strings("lumihost_restart").format(
                '<emoji document_id=5364105417569868801>😎</emoji> <b>LumiHost</b>'
                if self._client.hikka_me.premium
                and CUSTOM_EMOJIS
                and isinstance(msg_obj, Message)
                else "Netfoll"
            ),
        )

        await self.process_restart_message(msg_obj)

        self.set("restart_ts", time.time())

        await self._db.remote_force_save()

        if "LAVHOST" in os.environ:
            os.system("lavhost restart")
            return

        with contextlib.suppress(Exception):
            await main.hikka.web.stop()

        handler = logging.getLogger().handlers[0]
        handler.setLevel(logging.CRITICAL)

        for client in self.allclients:
            # Terminate main loop of all running clients
            # Won't work if not all clients are ready
            if client is not message.client:
                await client.disconnect()

        await message.client.disconnect()
        restart()

    async def download_common(self):
        try:
            repo = Repo(os.path.dirname(utils.get_base_dir()))
            origin = repo.remote("origin")
            r = origin.pull()
            new_commit = repo.head.commit
            for info in r:
                if info.old_commit:
                    for d in new_commit.diff(info.old_commit):
                        if d.b_path == "requirements.txt":
                            return True
            return False
        except git.exc.InvalidGitRepositoryError:
            repo = Repo.init(os.path.dirname(utils.get_base_dir()))
            origin = repo.create_remote("origin", self.config["GIT_ORIGIN_URL"])
            origin.fetch()
            repo.create_head("master", origin.refs.master)
            repo.heads.master.set_tracking_branch(origin.refs.master)
            repo.heads.master.checkout(True)
            return False

    @staticmethod
    def req_common():
        # Now we have downloaded new code, install requirements
        logger.debug("Installing new requirements...")
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.join(
                        os.path.dirname(utils.get_base_dir()),
                        "requirements.txt",
                    ),
                    "--user",
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            logger.exception("Req install failed")

    @loader.owner
    @loader.command(ru_doc="Скачивает обновления юзербота")
    async def update(self, message: Message):
        """Downloads userbot updates"""
        try:
            args = utils.get_args_raw(message)
            current = utils.get_git_hash()
            upcoming = next(
                git.Repo().iter_commits(f"origin/{version.branch}", max_count=1)
            ).hexsha
            if (
                "-f" in args
                or not self.inline.init_complete
                or not await self.inline.form(
                    message=message,
                    text=self.strings("update_confirm").format(
                        current, current[:8], upcoming, upcoming[:8]
                    )
                    if upcoming != current
                    else self.strings("no_update"),
                    reply_markup=[
                        {
                            "text": self.strings("btn_update"),
                            "callback": self.inline_update,
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                )
            ):
                raise
        except Exception:
            await self.inline_update(message)

    async def inline_update(
        self,
        msg_obj: typing.Union[InlineCall, Message],
        hard: bool = False,
    ):
        # We don't really care about asyncio at this point, as we are shutting down
        if hard:
            os.system(f"cd {utils.get_base_dir()} && cd .. && git reset --hard HEAD")

        try:
            if "" in os.environ:
                await self.process_restart_message(msg_obj)
                return

            with contextlib.suppress(Exception):
                msg_obj = await utils.answer(msg_obj, self.strings("downloading"))

            req_update = await self.download_common()

            with contextlib.suppress(Exception):
                msg_obj = await utils.answer(msg_obj, self.strings("installing"))

            if req_update:
                self.req_common()

            await self.restart_common(msg_obj)
        except GitCommandError:
            if not hard:
                await self.inline_update(msg_obj, True)
                return

            logger.critical("Got update loop. Update manually via .terminal")

    @loader.unrestricted
    @loader.command(ru_doc="Показать ссылку на исходный код проекта")
    async def source(self, message: Message):
        """Links the source code of this project"""
        await utils.answer(
            message,
            self.strings("source").format(self.config["GIT_ORIGIN_URL"]),
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
                                "netfoll-logs",
                                "netfoll-onload",
                                "netfoll-assets",
                                "netfoll-backups",
                                "netfoll-acc-switcher",
                                "silent-tags",
                            }
                            and dialog.is_channel
                            and (
                                dialog.entity.participants_count == 1
                                or dialog.entity.participants_count == 2
                                and dialog.name in {"netfoll-logs", "silent-tags"}
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
                "Can't create Netfoll folder. Possible reasons are:\n"
                "- User reached the limit of folders in Telegram\n"
                "- User got floodwait\n"
                "Ignoring error and adding folder addition to ignore list"
            )

    async def update_complete(self):
        logger.debug("Self update successful! Edit message")
        start = self.get("restart_ts")
        try:
            took = round(time.time() - start)
        except Exception:
            took = "n/a"

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
