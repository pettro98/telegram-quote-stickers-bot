import io
import asyncio

from PIL import Image

from sticker_builder import StickerBuilder
from util import get_project_abspath

MESSAGES = [
    "Lorem ipsum",
    "Another very very long Lorem ipsum text",
    "and a third text for good measure",
]

NICKNAME = "John Dick Doe"

AVATAR_PATH = get_project_abspath("assets/example_avatar.png")
AVATAR = Image.open(AVATAR_PATH)


async def main():
    sticker = StickerBuilder()

    sticker.set_nickname(NICKNAME)

    for txt in MESSAGES:
        sticker.add_message(txt)

    sticker.set_avatar(AVATAR)

    sticker.set_background((0x24, 0x30, 0x3f))
    sticker.set_accent((0x35, 0x7a, 0xcf))
    sticker.set_text_color((0xff, 0xff, 0xff))

    img_bytes = await sticker.build()

    sticker_img = Image.open(io.BytesIO(img_bytes))
    sticker_img.show("generated_sticker")

    pass


if __name__ == '__main__':
    asyncio.run(main())
