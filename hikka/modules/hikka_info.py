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
        "name": "HikkaInfo",
        "owner": "Owner",
        "version": "Version",
        "build": "Build",
        "prefix": "Prefix",
        "uptime": "Uptime",
        "branch": "Branch",
        "cpu_usage": "CPU usage",
        "ram_usage": "RAM usage",
        "send_info": "Send userbot info",
        "description": "ℹ This will not compromise any sensitive info",
        "up-to-date": (
            "<emoji document_id=5370699111492229743>😌</emoji> <b>Up-to-date</b>"
        ),
        "update_required": (
            "<emoji document_id=5424728541650494040>😕</emoji> <b>Update required"
            "</b> <code>.update</code>"
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
            "Custom message for info. May contain {me}, {version}, {build}, {prefix},"
            " {platform}, {upd}, {uptime}, {cpu_usage}, {ram_usage}, {branch} keywords"
        ),
        "_cfg_cst_btn": "Custom button for info. Leave empty to remove button",
        "_cfg_banner": "URL to image banner",
        "desc": (
            "<emoji document_id=6318565919471699564>🌌</emoji>"
            " <b>Hikka</b>\n\nTelegram userbot with a lot of features, like inline"
            " galleries, forms, lists and animated emojis support. Userbot - software,"
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
        "cpu_usage": "Использование CPU",
        "ram_usage": "Использование RAM",
        "send_info": "Отправить информацию о юзерботе",
        "description": "ℹ Это не раскроет никакой личной информации",
        "_ihandle_doc_info": "Отправить информацию о юзерботе",
        "up-to-date": (
            "<emoji document_id=5215191209131123104>💎</emoji> <b>Актуальная версия</b>"
        ),
        "update_required": (
            "<emoji document_id=5213383002129702114>🔔</emoji> <b>Требуется обновление"
            "</b> <code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "Кастомный текст сообщения в info. Может содержать ключевые слова {me},"
            " {version}, {build}, {prefix}, {platform}, {upd}, {uptime}, {cpu_usage},"
            " {ram_usage}, {branch}"
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
            "<emoji document_id=6318565919471699564>🌌</emoji>"
            " <b>Hikka</b>\n\nTelegram юзербот с огромным количеством функций, из"
            " которых: инлайн галереи, формы, списки, а также поддержка"
            " анимированных эмодзи. Юзербот - программа, которая запускается на"
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
                ["", ""],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Union(
                    loader.validators.Series(fixed_len=2),
                    loader.validators.NoneType(),
                ),
            ),
            loader.ConfigValue(
                "banner_url",
                "https://github.com/hikariatama/assets/raw/master/hikka_banner.mp4",
                lambda: self.strings("_cfg_banner"),
                validator=loader.validators.Link(),
            ),
        )

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
            self._client.hikka_me.id,
            utils.escape_html(get_display_name(self._client.hikka_me)),
        )
        build = utils.get_commit_url()
        _version = f'<i>{".".join(list(map(str, list(version.__version__))))}</i>'
        prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"

        platform = utils.get_named_platform()

        for emoji, icon in {
            "🍊": "<emoji document_id=5449599833973203438>🧡</emoji>",
            "🍇": "<emoji document_id=5449468596952507859>💜</emoji>",
            "❓": "<emoji document_id=5407025283456835913>📱</emoji>",
            "🍁": "<emoji document_id=6332120630099445554>🍁</emoji>",
            "🦾": "<emoji document_id=5386766919154016047>🦾</emoji>",
            "🚂": "<emoji document_id=5359595190807962128>🚂</emoji>",
            "🐳": "<emoji document_id=5431815452437257407>🐳</emoji>",
            "🕶": "<emoji document_id=5407025283456835913>📱</emoji>",
            "🐈‍⬛": "<emoji document_id=6334750507294262724>🐈‍⬛</emoji>",
            "✌️": "<emoji document_id=5469986291380657759>✌️</emoji>",
            "👾": "<emoji document_id=5370869711888194012>👾</emoji> ",
        }.items():
            platform = platform.replace(emoji, icon)

        return (
            (
                "<b>🌘 Hikka</b>\n"
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
                f" {self.strings('version')}:</b> {_version} {build}\n<b>{{}}"
                f" {self.strings('branch')}:"
                f"</b> <code>{version.branch}</code>\n{upd}\n\n<b>{{}}"
                f" {self.strings('prefix')}:</b> {prefix}\n<b>{{}}"
                f" {self.strings('uptime')}:"
                f"</b> {utils.formatted_uptime()}\n\n<b>{{}}"
                f" CPU and RAM usage: {utils.get_cpu_usage()}% | {utils.get_ram_usage()} MB\n"
                f"{platform}"
            ).format(
                *map(
                    lambda x: utils.remove_html(x) if inline else x,
                    (
                        utils.get_platform_emoji()
                        if self._client.hikka_me.premium and not inline
                        else "👾 Netfoll",
                        "<emoji document_id=5215327492738392838>🔩</emoji>",
                        "<emoji document_id=5215392879320505675>🛠</emoji>",
                        "<emoji document_id=5215263059639017128>👩‍💻</emoji>",
                        "<emoji document_id=5456222428730498101>😲</emoji>",
                        "<emoji document_id=5212928663309261889>⭐️</emoji>",
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
        thumb_url="https://img.icons8.com/external-others-inmotus-design/344/external-Moon-round-icons-others-inmotus-design-2.png"
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
        it_doc="Invia informazioni sul bot",
        de_doc="Sendet Informationen über den Bot",
        tr_doc="Bot hakkında bilgi gönderir",
        uz_doc="Bot haqida ma'lumot yuboradi",
        es_doc="Envía información sobre el bot",
        kk_doc="Бот туралы ақпарат жібереді",
    )
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
            await utils.answer_file(
                message,
                self.config["banner_url"],
                self._render_info(False),
            )

    @loader.unrestricted
    @loader.command(
        ru_doc="Отправить информацию по типу 'Что такое Хикка?'",
        it_doc="Invia informazioni del tipo 'Cosa è Hikka?'",
        de_doc="Sende Informationen über den Bot",
        tr_doc="Bot hakkında bilgi gönderir",
        uz_doc="Bot haqida ma'lumot yuborish",
        es_doc="Enviar información sobre el bot",
        kk_doc="Бот туралы ақпарат жіберу",
    )
    async def hikkainfo(self, message: Message):
        """Send info aka 'What is Hikka?'"""
        await utils.answer(message, self.strings("desc"))

    @loader.command(
        ru_doc="<текст> - Изменить текст в .info",
        it_doc="<testo> - Cambia il testo in .info",
        de_doc="<text> - Ändere den Text in .info",
        tr_doc="<metin> - .info'da metni değiştir",
        uz_doc="<matn> - .info'dagi matnni o'zgartirish",
        es_doc="<texto> - Cambiar el texto en .info",
        kk_doc="<мәтін> - .info мәтінін өзгерту",
    )
    async def setinfo(self, message: Message):
        """<text> - Change text in .info"""
        args = utils.get_args_html(message)
        if not args:
            return await utils.answer(message, self.strings("setinfo_no_args"))

        self.config["custom_message"] = args
        await utils.answer(message, self.strings("setinfo_success"))
