#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2023
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# Morri and Penggrin modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

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

    strings_ru = {
        "owner": "Владелец",
        "version": "Версия",
        "build": "Сборка",
        "prefix": "Префикс",
        "uptime": "Аптайм",
        "branch": "Ветка",
        "send_info": "Отправить информацию о юзерботе",
        "description": "ℹ Это не раскроет никакой личной информации",
        "_ihandle_doc_info": "Отправить информацию о юзерботе",
        "up-to-date": (
            ""
        ),
        "update_required": (
            "<emoji document_id=6334760737906362392>⚡</emoji> <b>Требуется обновление"
            "</b> <code>.update</code>\n"
        ),
        "_cfg_cst_msg": (
            "Кастомный текст сообщения в info. Может содержать ключевые слова {me},"
            " {version}, {prefix}, {platform}, {upd}, {uptime}, {cpu_usage},"
            " {ram_usage}"
        ),
        "_cfg_cst_btn": (
            "Кастомная кнопка в сообщении в info. Оставь пустым, чтобы убрать кнопку"
        ),
        "_cfg_banner": "Ссылка на баннер-картинку",
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>😢</emoji> <b>Тебе нужно указать"
            " текст для кастомного инфо</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>🎉</emoji> <b>Текст инфо успешно"
            " изменен</b>"
        ),
        "desc": (
            "<emoji document_id=4929415445443773080>🚀</emoji>"
            " <b>Netfoll</b>\n\nTelegram юзербот с огромным количеством функций, из"
            " которых: инлайн галереи, формы, списки основанных на Hikka. Юзербот - программа, которая запускается на"
            " твоем Telegram-аккаунте. Когда ты пишешь команду в любом чате, она"
            " сразу же выполняется. Обрати внимание на живые примеры на <a"
            ' href="https://github.com/MXRRI/Netfoll">GitHub</a>'
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                doc=lambda: self.strings("_cfg_cst_msg"),
            ),
            loader.ConfigValue(
                "custom_button",
                ["None", "None"],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Union(
                    loader.validators.Series(fixed_len=2),
                    loader.validators.NoneType(),
                ),
            ),
            loader.ConfigValue(
                "banner_url",
                "https://github.com/MXRRI/Netfoll/raw/stable/assets/banner.png",
                lambda: self.strings("_cfg_banner"),
                validator=loader.validators.Link(),
            ),
        )

    async def client_ready(self):
        self._me = await self._client.get_me()

        # Legacy migration
        if (
            self.config["banner_url"]
            == "https://github.com/MXRRI/Netfoll/raw/stable/assets/banner.png"
        ):
            self.config[
                "banner_url"
            ] = "https://github.com/MXRRI/Netfoll/raw/stable/assets/banner.png"

    def _render_info(self, inline: bool) -> str:
        try:
            repo = git.Repo(search_parent_directories=True)
            diff = repo.git.log([f"HEAD..origin/{version.branch}", "--oneline"])
            upd = (
                self.strings("update_required") if diff else self.strings("up-to-date")
            )
        except Exception:
            upd = ""

        me = '<b><a href="tg://user?id={}">{}</a></b>'.format(
            self._me.id,
            utils.escape_html(get_display_name(self._me)),
        )
        build = utils.get_commit_url()
        _version = f'<i>{version.branch} {".".join(list(map(str, list(version.netver))))}</i>'
        prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"

        platform = utils.get_named_platform()
       
        for emoji, icon in {
            "🍊": "<emoji document_id=5449599833973203438>🧡</emoji>",
            "🍇": "<emoji document_id=5449468596952507859>💜</emoji>",
            "❓": "<emoji document_id=5407025283456835913>📱</emoji>",
            "🍁": "<emoji document_id=5866334008123591985>💻</emoji>",
            "🦾": "<emoji document_id=5386766919154016047>🦾</emoji>",
            "🚂": "<emoji document_id=5359595190807962128>🚂</emoji>",
            "🐳": "<emoji document_id=5431815452437257407>🐳</emoji>",
            "🕶": "<emoji document_id=5407025283456835913>📱</emoji>",
            "🐈‍⬛": "<emoji document_id=6334750507294262724>🐈‍⬛</emoji>",
            "✌️": "<emoji document_id=5469986291380657759>✌️</emoji>",
            "👾": "<emoji document_id=5866169914603081371>🐧</emoji> ",
        }.items():
            platform = platform.replace(emoji, icon)

        return (
            (
                "\n"
                if "hikka" not in self.config["custom_message"].lower()
                else ""
            )
            + self.config["custom_message"].format(
                me=me,
                version=_version,
                build=build,
                prefix=prefix,
                platform=platform,
                upd=upd,
                uptime=utils.formatted_uptime(),
                cpu_usage=utils.get_cpu_usage(),
                ram_usage=f"{utils.get_ram_usage()} MB",
                branch=version.branch,
            )
            if self.config["custom_message"]
            else (
                f'<b>{{}} for <b>{me}</b></b>\n\n{{}}'
                f" <b>{self.strings('version')}:</b> {_version} {build}<b>\n"
                f"</b>{upd}\n<b>{{}}"
                f" <b>{self.strings('prefix')}:</b> {prefix}\n<b>{{}}"
                f" <b>{self.strings('uptime')}:"
                f"</b> {utils.formatted_uptime()}\n\n<b>{{}}"
                f"<b>{platform} ({utils.get_cpu_usage()}% | {utils.get_ram_usage()})</b>"
            ).format(
                *map(
                    lambda x: utils.remove_html(x) if inline else x,
                    (
                        utils.get_platform_emoji()
                        if self._client.hikka_me.premium and not inline
                        else "👾 Netfoll",
                        "<emoji document_id=6334456392228800167>🪢</emoji>",
                        "<emoji document_id=6334701737940616970>💫</emoji>",
                        "<emoji document_id=6334620339720423126>🕛</emoji>",
                        "<emoji document_id=6334685601748486176>🎨</emoji>",
                    ),
                )
            )
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
                "hhttps://github.com/MXRRI/Netfoll/raw/Stable/assets/bot_pfp.png"
            ),
            "reply_markup": self._get_mark(),
        }

    @loader.unrestricted
    async def infocmd(self, message: Message):
        """Send userbot info"""

        if self.config["custom_button"]:
            await self.inline.form(
                message=message,
                text=self._render_info(True),
                reply_markup=self._get_mark(),
                **(
                    {"photo": self.config["banner_url"]}
                    if self.config["banner_url"]
                    else {}
                ),
            )
        else:
            try:
                await self._client.send_file(
                    message.peer_id,
                    self.config["banner_url"],
                    caption=self._render_info(False),
                )
            except Exception:
                await utils.answer(message, self._render_info(False))
            else:
                if message.out:
                    await message.delete()

    @loader.unrestricted
    @loader.command(
        ru_doc="Отправить информацию по типу 'Что такое Netfoll?'",
    )
    async def whonetfoll(self, message: Message):
        """Send info aka 'What is Hikka?'"""
        await utils.answer(message, self.strings("desc"))

    @loader.command(
        ru_doc="<текст> - Изменить текст в .info",
    )
    async def setinfo(self, message: Message):
        """<text> - Change text in .info"""
        args = utils.get_args_html(message)
        if not args:
            return await utils.answer(message, self.strings("setinfo_no_args"))

        self.config["custom_message"] = args
        await utils.answer(message, self.strings("setinfo_success"))
