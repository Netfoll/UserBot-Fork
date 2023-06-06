#
# 🔒 The MIT License (MIT)
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#
# ---------------------------------------------------------------------------------
#     ▀▄   ▄▀   👾 Module for Netfoll User Bot (based on Hikka 1.6.0)
#    ▄█▀███▀█▄  🔒 The MIT License (MIT)
#   █▀███████▀█ ⚠️ Owner @DarkModules and @Netfoll
#   █ █▀▀▀▀▀█ █
#      ▀▀ ▀▀
# ---------------------------------------------------------------------------------
# meta developer: @Netfoll

import difflib
import inspect
import io

from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class ModuleCloudMod(loader.Module):
    """Hikari modules management"""

    strings = {
        "name": "ModuleCloud",
        "args": "🚫 <b>Args not specified</b>",
        "404": "😔 <b>Module not found</b>",
        "not_exact": (
            "⚠️ <b>No exact match occured, so the closest result is shown instead</b>"
        ),
    }

    strings_ru = {
        "args": "🚫 <b>Нет аргументов</b>",
        "_cls_doc": "Поиск модулей",
        "not_exact": (
            "⚠️ <b>Точного совпадения не нашлось, поэтому был выбран наиболее"
            " подходящее</b>"
        ),
        "404": "😔 <b>Модуль не найден</b>",
    }

    @loader.command(
        ru_doc="<имя модуля> - Отправить ссылку на модуль",
    )
    async def ml(self, message: Message):
        """<module name> - Send link to module"""
        args = utils.get_args_raw(message)
        exact = True
        if not args:
            await utils.answer(message, self.strings("args"))
            return

        try:
            try:
                class_name = next(
                    module.strings["name"]
                    for module in self.allmodules.modules
                    if args.lower() == module.strings["name"].lower()
                )
            except Exception:
                try:
                    class_name = next(
                        reversed(
                            sorted(
                                [
                                    module.strings["name"]
                                    for module in self.allmodules.modules
                                ],
                                key=lambda x: difflib.SequenceMatcher(
                                    None,
                                    args.lower(),
                                    x,
                                ).ratio(),
                            )
                        )
                    )
                    exact = False
                except Exception:
                    await utils.answer(message, self.strings("404"))
                    return

            module = next(
                filter(
                    lambda mod: class_name.lower() == mod.strings["name"].lower(),
                    self.allmodules.modules,
                )
            )

            sys_module = inspect.getmodule(module)

            link = module.__origin__

            text = (
                f"<b>🧳 {utils.escape_html(class_name)}</b>"
                if not utils.check_url(link)
                else (
                    f'📼 <b><a href="{link}">Link</a> for'
                    f" {utils.escape_html(class_name)}:</b>"
                    f' <code>{link}</code>\n\n{self.strings("not_exact") if not exact else ""}'
                )
            )

            file = io.BytesIO(sys_module.__loader__.data)
            file.name = f"{class_name}.py"
            file.seek(0)

            await message.respond(text, file=file)

            if message.out:
                await message.delete()
        except Exception:
            await utils.answer(message, self.strings("404"))
