# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

import asyncio
import contextlib

import git

from .. import loader, utils, version
from ..inline.types import InlineCall


@loader.tds
class UpdateNotifierMod(loader.Module):
    """Tracks latest Netfoll releases, and notifies you, if update is required"""

    strings = {
        "name": "UpdateNotifier",
        "update_required": (
            "👾 <b>Netfoll Update available!</b>\n\nNew Netfoll version released.\n💿"
            " <b>Netfoll <s>{}</s> -> {}</b>\n\nChanges: 👇🏻\n\n{}"
        ),
        "more": "\n<i><b>🎥 And {} more...</b></i>",
        "_cfg_doc_disable_notifications": "Disable update notifications",
        "latest_disabled": "Notifications about the latest update have been suppressed",
        "update": "🔄 Update",
        "ignore": "🚫 Ignore",
    }

    strings_ru = {
        "update_required": (
            "👾 <b>Новая версия Netfoll!</b>\n\nВ GitHub вышла новая версия.\n💿"
            " <b>Netfoll <s>{}</s> -> {}</b>\n\nИзменения: 👇🏻\n\n{}"
        ),
        "more": "\n<i><b>🎥 И еще {}...</b></i>",
        "_cfg_doc_disable_notifications": "Отключить уведомления об обновлениях",
        "latest_disabled": "Уведомления о последнем обновлении были отключены",
        "update": "🔄 Обновить",
        "ignore": "🚫 Игнорировать",
    }

    strings_uk = {
        "update_required": (
            "👾 <b>Нова версія Netfoll!</b>\n\nВ GitHub вийшла нова версія.\n💿"
            " <b>Netfoll <s>{}</s> -> {}</b>\n\nИзменения: 👇🏻\n\n{}"
        ),
        "more": "\n<i><b>🎥 І ще {}...</b></i>",
        "_cfg_doc_disable_notifications": "Вимкнути сповіщення про оновлення",
        "latest_disabled": "Повідомлення про останнє оновлення були відключені",
        "update": "🔄 Оновити",
        "ignore": "🚫 Ігнорувати",
    }

    _notified = None

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "disable_notifications",
                doc=lambda: self.strings("_cfg_doc_disable_notifications"),
                validator=loader.validators.Boolean(),
            )
        )

    def get_changelog(self) -> str:
        try:
            repo = git.Repo()

            for remote in repo.remotes:
                remote.fetch()

            if not (
                diff := repo.git.log([f"HEAD..origin/{version.branch}", "--oneline"])
            ):
                return False
        except Exception:
            return False

        res = "\n".join(
            f"<b>{commit.split()[0]}</b>:"
            f" <i>{utils.escape_html(' '.join(commit.split()[1:]))}</i>"
            for commit in diff.splitlines()[:10]
        )

        if diff.count("\n") >= 10:
            res += self.strings("more").format(len(diff.splitlines()) - 10)

        return res

    def get_latest(self) -> str:
        try:
            return list(
                git.Repo().iter_commits(f"origin/{version.branch}", max_count=1)
            )[0].hexsha
        except Exception:
            return ""

    async def client_ready(self):
        await utils.convert_folders(self.client)

        try:
            git.Repo()
        except Exception as e:
            raise loader.LoadError("Can't load due to repo init error") from e

        self._markup = lambda: self.inline.generate_markup(
            [
                {"text": self.strings("update"), "data": "netfoll_update"},
                {"text": self.strings("ignore"), "data": "netfoll_upd_ignore"},
            ]
        )

        self.poller.start()

    @loader.loop(interval=60)
    async def poller(self):
        if self.config["disable_notifications"] or not self.get_changelog():
            return

        self._pending = self.get_latest()

        if (
            self.get("ignore_permanent", False)
            and self.get("ignore_permanent") == self._pending
        ):
            await asyncio.sleep(60)
            return

        if self._pending not in [utils.get_git_hash(), self._notified]:
            m = await self.inline.bot.send_message(
                self.tg_id,
                self.strings("update_required").format(
                    utils.get_git_hash()[:6],
                    '<a href="https://github.com/MXRRI/Netfoll/compare/{}...{}">{}</a>'
                    .format(
                        utils.get_git_hash()[:12],
                        self.get_latest()[:12],
                        self.get_latest()[:6],
                    ),
                    self.get_changelog(),
                ),
                disable_web_page_preview=True,
                reply_markup=self._markup(),
            )

            self._notified = self._pending
            self.set("ignore_permanent", False)

            await self._delete_all_upd_messages()

            self.set("upd_msg", m.message_id)

    async def _delete_all_upd_messages(self):
        for client in self.allclients:
            with contextlib.suppress(Exception):
                await client.loader.inline.bot.delete_message(
                    client.tg_id,
                    client.loader.db.get("UpdateNotifierMod", "upd_msg"),
                )

    @loader.callback_handler()
    async def update(self, call: InlineCall):
        """Process update buttons clicks"""
        if call.data not in {"netfoll_update", "netfoll_upd_ignore"}:
            return

        if call.data == "netfoll_upd_ignore":
            self.set("ignore_permanent", self.get_latest())
            await call.answer(self.strings("latest_disabled"))
            return

        await self._delete_all_upd_messages()

        with contextlib.suppress(Exception):
            await call.delete()

        await self.invoke("update", "-f", peer=self.inline.bot_username)
