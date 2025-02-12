import base64

import pyppeteer
import pyrogram as pg
import pyrogram.types as pg_t
import pyrogram.filters as pg_flt
import PIL
import sqlite3
import asyncio
import os
import sys
import io
import argparse
import jinja2

from bot_utils import timed_zone
from user_db import UserDB, MemoryUserDBImpl, UserDrawingSettings
from draw_sticker import render_sticker, PrivateDrawingSettings
from PIL import Image


# TODO: stickers from forwarded messages
# TODO: stickers from replied messages (via bot mentioning in reply)
# TODO: stickers from several messages
# TODO: send stickers as pictures and as documents ( if sent file is .webp then telegram automatically shows it as a sticker)

# TODO: store user template settings
# TODO: inline commands if used via reply
# TODO: one-shot settings vs persistent settings
# TODO: Versioning settings structure
# TODO: send error messages to owners telegram messages if --alert_user_id specified

# TODO: change background color
# TODO: select avatar (or no avatar/generated standard avatars) (check telegram apis for situations with no custom picture)
# TODO: respect rich text/markdown
# TODO: select/respect username color
# TODO: show/change preview of sticker
# TODO: possibility to edit sticker from forwarded message before creating
# TODO: import colors from user-provided theme (maybe via link)
# TODO: support different user themes (check mobile themes for reference) - add,remove,edit,switch_active

# FIXME: second name if not present, renders to None
# FIXME: very long names will go out of bounds
async def main():
    args = argparse.ArgumentParser(description="Telegram bot to create sticker images from messages",
                                   fromfile_prefix_chars="@")
    args.add_argument("--api_id", type=int, required=True)  # pyrogram still needs id and hash for MTProto to work
    args.add_argument("--api_hash", type=str, required=True)
    args.add_argument("--bot_token", type=str, required=True)
    # args.add_argument("--alert_user_id", default=None)
    parsed_args = args.parse_args()

    user_db: UserDB
    user_db = MemoryUserDBImpl()

    app = pg.Client("bot", **vars(parsed_args))

    browser = await pyppeteer.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--no-zygote-sandbox",
            "--incognito",
        ])

    drawing_env = jinja2.Environment(loader=jinja2.FileSystemLoader(["assets"]))

    @app.on_message(filters=pg_flt.incoming & pg_flt.private)
    async def handle_personal_message(client: pg.Client, message: pg_t.Message):
        user_drawing_settings = UserDrawingSettings()
        avatar_data = io.BytesIO()
        avatar_format = ""
        photos = client.get_chat_photos(message.from_user.username, limit=1)
        async for photo in photos:
            for thumb in photo.thumbs:
                if thumb.width != 160:
                    continue
                avatar_data = await client.download_media(thumb.file_id, in_memory=True)
                break

        if len(avatar_data.getvalue()) != 0:
            avatar_format = Image.open(avatar_data).format.lower()
        else:
            await message.reply("Could not get profile photo")

        private_drawing_settings = PrivateDrawingSettings(
            user_name=([] if message.from_user.first_name is None else [message.from_user.first_name]) + (
                [] if message.from_user.last_name is None else [message.from_user.last_name]),
            messages=[message.text],
            user_color_real="cyan",
            avatar_mime="image/" + avatar_format.lower(),
            avatar_data=avatar_data.getvalue())

        sticker_blob = await render_sticker(browser, drawing_env, user_drawing_settings, private_drawing_settings)

        sticker_io = io.BytesIO(sticker_blob)
        sticker_io.name = "sticker.webp"
        await message.reply_sticker(sticker_io)

    await app.start()
    await pg.idle()
    await app.stop()

    await browser.close()


asyncio.run(main())
