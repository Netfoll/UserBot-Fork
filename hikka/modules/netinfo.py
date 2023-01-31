# ©️ Dan Gazizullin, 2021-2022
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import git
from telethon.tl.types import Message
from telethon.utils import get_display_name

from .. import loader, utils, version
from ..inline.types import InlineQuery


@loader.tds
class HikkaInfoMod(loader.Module):
    """Show userbot info"""

    strings = {
        "name": "Info",
        "owner": "Owner",
        "version": "Version",
        "build": "Build",
        "prefix": "Prefix",
        "uptime": "Uptime",
        "branch": "Branch",
        "send_info": "Send userbot info",
        "description": "ℹ This will not compromise any sensitive info",
        "up-to-date": (
            ""
        ),
        "update_required": (
            "<emoji document_id=6334760737906362392>⚡</emoji> <b>Update required"
            "</b> <code>.update</code>\n"
        ),
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>😢</emoji> <b>You need to specify"
            " text to change info to</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>🎉</emoji> <b>Info changed"
            " successfully</b>"
        ),
        "_cfg_cst_msg": (
            "Custom message for info. May contain {me}, {version}, {prefix},"
            " {platform}, {upd}, {uptime}, {cpu_usage}, {ram_usage} keywords"
        ),
        "_cfg_cst_btn": "Custom button for info. Leave empty to remove button",
        "_cfg_banner": "URL to image banner",
        "desc": (
            "<emoji document_id=4929415445443773080>🚀</emoji>"
            " <b>Netfoll</b>\n\nTelegram userbot with a lot of features, like inline"
            " galleries, forms, lists lists based on Hikka. Userbot - software,"
            " running on your Telegram account. If you write a command to any chat, it"
            " will get executed right there. Check out live examples at <a"
            ' href="https://github.com/MXRRI/Netfoll">GitHub</a>'
        ),
    }

    def _render_info(self, inline: bool) -> str:
        me = '<b><a href="tg://user?id={}">{}</a></b>'.format(
            self._client.hikka_me.id,
            utils.escape_html(get_display_name(self._client.hikka_me)),
        )
        build = utils.get_commit_url()
        prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"
        platform = utils.get_named_platform()
        me=me,
        build=build,
        prefix=prefix,
        platform=platform,
        uptime=utils.formatted_uptime(),
        branch=version.branch,

        return (
                f'<b>{{}} for <b>{me}</b></b>\n\n{{}}'
                f" <b>{self.strings('version')}:</b> {version} {build}<b>\n"
                f" <b>{self.strings('prefix')}:</b> {prefix}\n<b>{{}}"
                f" <b>{self.strings('uptime')}:"
                f"</b> {utils.formatted_uptime()}\n\n<b>{{}}"
                f"<b>{platform} ({utils.get_cpu_usage()}% | {utils.get_ram_usage()} RAM)</b>"
            )

    def _get_mark(self):
        return (
            {
                "text": self.config["custom_button"][0],
                "url": self.config["custom_button"][1],
            }
            if self.config["custom_button"]
            else None
        )

    @loader.inline_handler(
        thumb_url="https://img.icons8.com/nolan/512/info-squared.png"
    )
    @loader.inline_everyone
    async def info(self, _: InlineQuery) -> dict:
        """Send userbot info"""

        return {
            "title": self.strings("send_info"),
            "description": self.strings("description"),
            **(
                {"photo": self.config["banner_url"], "caption": self._render_info(True)}
                if self.config["banner_url"]
                else {"message": self._render_info(True)}
            ),
            "thumb": (
                "https://github.com/hikariatama/Hikka/raw/master/assets/hikka_pfp.png"
            ),
            "reply_markup": self._get_mark(),
        }

    @loader.command(
        ru_doc="Отправляет информацию о боте",
        alias="инфо"
    )
    @loader.unrestricted
    async def infocmd(self, message: Message):
        """Send userbot info"""

        await utils.answer(
                message,
                self._render_info(message),
            )