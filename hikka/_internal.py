# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# 🌐 https://github.com/MXRRI/Netfoll

import asyncio
import atexit
import logging
import os
import random
import signal
import sys


async def fw_protect():
    await asyncio.sleep(random.randint(1000, 3000) / 1000)


def get_startup_callback() -> callable:
    return lambda *_: os.execl(
        sys.executable,
        sys.executable,
        "-m",
        os.path.relpath(os.path.abspath(os.path.dirname(os.path.abspath(__file__)))),
        *sys.argv[1:],
    )


def die():
    if "DOCKER" in os.environ:
        sys.exit(0)
    else:
        os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)


def restart():
    if "HIKKA_DO_NOT_RESTART" in os.environ:
        print(
            "Got in a loop, exiting\nYou probably need to manually remove existing"
            " packages and then restart Netfoll. Run `pip uninstall -y telethon"
            " telethon-mod hikka-tl pyrogram hikka-pyro`, then restart Netfoll."
        )
        sys.exit(0)

    logging.getLogger().setLevel(logging.CRITICAL)

    print("🔄 Restarting...")

    if "LAVHOST" in os.environ:
        os.system("lavhost restart")
        return

    os.environ["HIKKA_DO_NOT_RESTART"] = "1"
    if "DOCKER" in os.environ:
        atexit.register(get_startup_callback())
    else:
        signal.signal(signal.SIGTERM, get_startup_callback())

    die()
