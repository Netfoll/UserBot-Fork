# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the Copyleft license.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: profile
# Description: Module for get beautiful picture profile statistic
# Author: vsecoder
# Commands:
# .profile
# ---------------------------------------------------------------------------------


"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2022 t.me/vsecoder                                                            
    This program is free software; you can redistribute it and/or modify 

"""
# meta developer: @vsecoder_m
# meta pic: https://img.icons8.com/office/344/administrator-male--v1.png

__version__ = (0, 0, 1)

import logging
from .. import loader, utils
from telethon import functions
import imgkit
import base64
import requests


logger = logging.getLogger(__name__)


@loader.tds
class Profilemod(loader.Module):
    """Module for get beautiful picture profile statistic"""

    strings = {"name": "Profilemod"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "background",
                "https://0x0.st/oSzw.jpg",
                "Url to background (540x220 is perfect)",
                validator=loader.validators.Link(),
            ),
            loader.ConfigValue(
                "html_template",
                "https://raw.githubusercontent.com/vsecoder/hikka_modules/main/assets/profile.html",
                "link to html template (if you don't know how, don't touch!)",
                validator=loader.validators.Link(),
            ),
        )
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.unrestricted
    @loader.ratelimit
    async def profilecmd(self, message):
        """
        - get
        """
        chats, channels, bots, users = 0, 0, 0, 0
        message = await utils.answer(message, "Geting profile info...")
        async for dialog in self._client.iter_dialogs(ignore_migrated=True):
            if dialog.is_group:
                chats += 1
            elif dialog.is_channel:
                channels += 1
            elif dialog.entity.bot:
                bots += 1
            else:
                users += 1

        options = {"crop-w": 540, "crop-h": 220, "encoding": "UTF-8"}

        me = await self._client.get_me()
        desc = await self._client(functions.users.GetFullUserRequest(me.id))

        message = await utils.answer(message, "Downloading profile photo...")
        await self._client.download_profile_photo("me", "profile.jpg")
        message = await utils.answer(message, "Converting profile photo...")
        base64EncodedStr = base64.b64encode(open("profile.jpg", "rb").read()).decode(
            "utf-8"
        )

        message = await utils.answer(message, "Formating info to template...")
        with open("profile.html", "w") as f:
            template = requests.get(self.config["html_template"]).text
            f.write(
                template.format(
                    self.config["background"],
                    base64EncodedStr,
                    f"@{me.username}",
                    chats,
                    channels,
                    users,
                    bots,
                    desc.full_user.about,
                )
            )

        message = await utils.answer(message, "Converting to image...")
        wkhtmltopdf = 'C:\Program Files\wkhtmltopdf'
        imgkit.from_file("profile.html", "profile.jpg", options=options)
        message = await utils.answer(message, "Complete:")

        await self._client.send_file(
            utils.get_chat_id(message),
            open("profile.jpg", "rb"),
        )