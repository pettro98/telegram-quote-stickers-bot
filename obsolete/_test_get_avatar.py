import argparse

import pyrogram
from PIL import Image

args = argparse.ArgumentParser(fromfile_prefix_chars="@")
args.add_argument("--api_id", type=int, required=True)
args.add_argument("--api_hash", type=str, required=True)
args.add_argument("--bot_token", type=str, required=True)
parsed_args = args.parse_args(["@config.txt"])

app = pyrogram.Client(name="bot", **vars(parsed_args))


@app.on_message(filters=pyrogram.filters.incoming & pyrogram.filters.private)
async def echo_avatar(client: pyrogram.Client, message: pyrogram.types.Message):
    photos = client.get_chat_photos(message.from_user.username)
    got_any_photos = False
    async for photo in photos:
        got_any_photos = True
        image_blob = await client.download_media(photo.file_id)
        Image.open(image_blob).show()
        print(f"Got photo size: {photo.width}x{photo.height}")
        for thumb in photo.thumbs:
            image_blob = await client.download_media(thumb.file_id)
            Image.open(image_blob).show()
            print(f"Got thumb size: {thumb.width}x{thumb.height}")

    if not got_any_photos:
        print("cannot get any user photos")


app.add_handler(pyrogram.handlers.MessageHandler(echo_avatar))
app.run()
