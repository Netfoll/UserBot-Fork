#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

# meta pic: https://static.hikari.gay/cloud_icon.png
# meta banner: https://mods.hikariatama.ru/badges/cloud.jpg
# meta developer: @hikarimods


import difflib
import inspect
import io


from telethon.tl.custom import Message


from .. import loader, utils


@loader.tds
class ModuleCloudMod(loader.Module):
    """Modules management"""

    strings = {
        "name": "ModuleCloud",
        "args": "🚫 <b>Args not specified</b>",
        "404": "🚫 <b>Module {} not found</b>",
        "no_link": "<b>🧳 {class_name}</b>",
        "link_for": (
            '📼 <b><a href="{link}">Link</a> for'
            " {class_name}:</b>"
            " <code>{link}</code>"
        ),
        "not_exact": (
            "⚠️ <b>No exact match occured, so the closest result is shown instead</b>"
        ),
    }

    strings_ru = {
        "args": "🚫 <b>Нет аргументов</b>",
        "404": "🚫 <b>Модуль {} не найден</b>",
        "link_for": (
            '📼 <b><a href="{link}">Ссылка</a> на'
            " {class_name}:</b>"
            " <code>{link}</code>"
        ),
        "not_exact": (
            "⚠️ <b>Точного совпадения не нашлось, поэтому был выбрано наиболее"
            " подходящее</b>"
        ),
    }

    @loader.command(
        ru_doc="<имя модуля> - Отправить ссылку на модуль",
    )
    async def mlcmd(self, message: Message):
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
                    await utils.answer(
                        message, self.strings("404").format(utils.escape_html(args))
                    )
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
                self.strings["no_url"].format(class_name=utils.escape_html(class_name))
                if not utils.check_url(link)
                else self.strings["link_for"].format(
                    link=link, class_name=utils.escape_html(class_name)
                )
            )

            file = io.BytesIO(sys_module.__loader__.data)
            file.name = f"{class_name}.py"
            file.seek(0)

            await message.respond(text, file=file, reply_to=utils.get_topic(message))

            if message.out:
                await message.delete()

        except Exception:
            await utils.answer(
                message, self.strings("404").format(utils.escape_html(args))
            )
