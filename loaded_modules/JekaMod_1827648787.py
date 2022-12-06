# Name: ЖекаБот
# Description: Легкое использование ЖекаБот'а @just_zhenya_bot
# Author: Morri
# Commands:
# .дем .эдвайс .жмых .кек .кеклол .жпег .вьетнам .тлен
# ---------------------------------------------------------------------------------


# meta developer: @HikkaWE


from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError 

from .. import loader, utils


@loader.tds
class JekaMod(loader.Module):
    """Модуль ЖекаБот - @just_zhenya_bot"""

    strings = {"name": "ЖекаБот"}

    @loader.owner
    async def демcmd(self, message):
        """Демотивировать: Например (.дем Люти/Пон)"""
        demik = "/дем "
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.edit("<b>Ответь на фото</b>")
        try:
            media = reply.media
        except Exception:
            return await message.edit("<b>Только фото</b>")
        chat = "@just_zhenya_bot"
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=528677877)
                )
                mm = await message.client.send_file(chat, media, caption=demik + args)
                response = await response
                await mm.delete()
            except YouBlockedUserError:
                return await message.reply(
                    "<b>Разблокируй @just_zhenya_bot</b>"
                )
            await message.delete()
            await response.delete()
            await message.client.send_file(
                message.to_id,
                response.media,
                reply_to=await message.get_reply_message(),
            )   
            
    
    async def эдвайсcmd(self, message):
        """Сделать мемчик на фото (.эдвайс СУПЕР/ПУПЕР)"""
        edvice = "/эдвайс "
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.edit("<b>Ответь на фото</b>")
        try:
            media = reply.media
        except Exception:
            return await message.edit("<b>Только фото</b>")
        chat = "@just_zhenya_bot"
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=528677877)
                )
                mm = await message.client.send_file(chat, media, caption=edvice + args)
                response = await response
                await mm.delete()
            except YouBlockedUserError:
                return await message.reply(
                    "<b>Разблокируй @just_zhenya_bot</b>"
                )
            await message.delete()
            await response.delete()
            await message.client.send_file(
                message.to_id,
                response.media,
                reply_to=await message.get_reply_message(),
            )             
            
    async def жмыхcmd(self, message):
        """Жмыхнуть фото"""
        jmih = "/жмых"
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.edit("<b>Ответь на фото</b>")
        try:
            media = reply.media
        except Exception:
            return await message.edit("<b>Только фото</b>")
        chat = "@just_zhenya_bot"
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=528677877)
                )
                mm = await message.client.send_file(chat, media, caption=jmih)
                response = await response
                await mm.delete()
            except YouBlockedUserError:
                return await message.reply(
                    "<b>Разблокируй @just_zhenya_bot</b>"
                )
            await message.delete()
            await response.delete()
            await message.client.send_file(
                message.to_id,
                response.media,
                reply_to=await message.get_reply_message(),
            )
            
    async def кекcmd(self, message):
        """Отзеркалить фото"""
        kek = "/кек"
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.edit("<b>Ответь на фото</b>")
        try:
            media = reply.media
        except Exception:
            return await message.edit("<b>Только фото</b>")
        chat = "@just_zhenya_bot"
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=528677877)
                )
                mm = await message.client.send_file(chat, media, caption=kek)
                response = await response
                await mm.delete()
            except YouBlockedUserError:
                return await message.reply(
                    "<b>Разблокируй @just_zhenya_bot</b>"
                )
            await message.delete()
            await response.delete()
            await message.client.send_file(
                message.to_id,
                response.media,
                reply_to=await message.get_reply_message(),
            )            

    async def кеклолcmd(self, message):
        """Отзеркалить в другую сторону"""
        keklol = "/кек лол"
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.edit("<b>Ответь на фото</b>")
        try:
            media = reply.media
        except Exception:
            return await message.edit("<b>Только фото</b>")
        chat = "@just_zhenya_bot"
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=528677877)
                )
                mm = await message.client.send_file(chat, media, caption=keklol)
                response = await response
                await mm.delete()
            except YouBlockedUserError:
                return await message.reply(
                    "<b>Разблокируй @just_zhenya_bot</b>"
                )
            await message.delete()
            await response.delete()
            await message.client.send_file(
                message.to_id,
                response.media,
                reply_to=await message.get_reply_message(),
            )          

    async def жпегcmd(self, message):
        """Жпегнуть фото"""
        hakal = "/жпег"
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.edit("<b>Ответь на фото</b>")
        try:
            media = reply.media
        except Exception:
            return await message.edit("<b>Только фото</b>")
        chat = "@just_zhenya_bot"
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=528677877)
                )
                mm = await message.client.send_file(chat, media, caption=hakal)
                response = await response
                await mm.delete()
            except YouBlockedUserError:
                return await message.reply(
                    "<b>Разблокируй @just_zhenya_bot</b>"
                )
            await message.delete()
            await response.delete()
            await message.client.send_file(
                message.to_id,
                response.media,
                reply_to=await message.get_reply_message(),
            )

    async def вьетнамcmd(self, message):
        """Наложить Вьетнам на фото"""
        vietnam = "/вьетнам"
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.edit("<b>Ответь на фото</b>")
        try:
            media = reply.media
        except Exception:
            return await message.edit("<b>Только фото</b>")
        chat = "@just_zhenya_bot"
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=528677877)
                )
                mm = await message.client.send_file(chat, media, caption=vietnam)
                response = await response
                await mm.delete()
            except YouBlockedUserError:
                return await message.reply(
                    "<b>Разблокируй @just_zhenya_bot</b>"
                )
            await message.delete()
            await response.delete()
            await message.client.send_file(
                message.to_id,
                response.media,
                reply_to=await message.get_reply_message(),
            )              
            
    async def тленcmd(self, message):
        """Наложить тлен на фото"""
        tlen = "/тлен"
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.edit("<b>Ответь на фото</b>")
        try:
            media = reply.media
        except Exception:
            return await message.edit("<b>Только фото</b>")
        chat = "@just_zhenya_bot"
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=528677877)
                )
                mm = await message.client.send_file(chat, media, caption=tlen)
                response = await response
                await mm.delete()
            except YouBlockedUserError:
                return await message.reply(
                    "<b>Разблокируй @just_zhenya_bot</b>"
                )
            await message.delete()
            await response.delete()
            await message.client.send_file(
                message.to_id,
                response.media,
                reply_to=await message.get_reply_message(),
            )                 