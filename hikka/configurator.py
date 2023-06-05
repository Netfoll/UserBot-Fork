#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2021 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

import locale
import os
import string
import sys
import typing

from dialog import Dialog, ExecutableNotFound

from . import utils


def _safe_input(*args, **kwargs):
    try:
        return input(*args, **kwargs)
    except (EOFError, OSError):
        raise
    except KeyboardInterrupt:
        print()
        return None


class TDialog:
    def inputbox(self, query: str) -> typing.Tuple[bool, str]:
        print(query)
        print()
        inp = _safe_input("Введите значение...:")
        return (False, "Cancelled") if not inp else (True, inp)

    def msgbox(self, msg: str) -> bool:
        print(msg)
        return True


TITLE = ""

if sys.stdout.isatty():
    try:
        DIALOG = TDialog()
    except (ExecutableNotFound, locale.Error):
        DIALOG = Dialog(dialog="dialog", autowidgetsize=True)
        locale.setlocale(locale.LC_ALL, "")
else:
    DIALOG = TDialog()


def api_config(data_root: str):
    code, hash_value = DIALOG.inputbox(
        """­



















 _   _      _    __       _ _ 
| \ | | ___| |_ / _| ___ | | |
|  \| |/ _ \ __| |_ / _ \| | |
| |\  |  __/ |_|  _| (_) | | |
|_| \_|\___|\__|_|  \___/|_|_|

Пожалуйста, введите API HASH
Для отмены, нажмите Ctrl + Z
    """
    )
    if not code:
        return

    if len(hash_value) != 32 or any(it not in string.hexdigits for it in hash_value):
        DIALOG.msgbox("Неверный HASH")
        return

    code, id_value = DIALOG.inputbox(
        """­
Отлично! Теперь введите API ID
    """
    )

    if not id_value or any(it not in string.digits for it in id_value):
        DIALOG.msgbox("Неверный ID")
        return

    with open(
        os.path.join(
            data_root or os.path.dirname(utils.get_base_dir()), "api_token.txt"
        ),
        "w",
    ) as file:
        file.write(id_value + "\n" + hash_value)

    DIALOG.msgbox(
        "API данные сохранены. Осталось только ввести номер и код подтверждения. Приступим!\n"
    )
