import io
import asyncio

from PIL import Image, ImageDraw, ImageOps
from util import get_project_abspath
import jinja2

ROBOTO_AVATAR_PATH = get_project_abspath("assets/Roboto-Bold.ttf")


async def main():
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('../assets'), undefined=jinja2.StrictUndefined)

    stub_avatar = Image.new(mode="RGB", size=(50, 50), color=(255, 255, 255))
    draw_context = ImageDraw.Draw(stub_avatar)
    draw_context.line((50, 50) + (0, 0), fill=(255, 0, 0), width=4)
    stub_avatar_data = io.BytesIO()
    stub_avatar.save(stub_avatar_data, format="PNG")

    # image = await render_sticker(jinja_env, UserDrawingSettings(),
    #                              PrivateDrawingSettings("image/png", stub_avatar_data.getvalue(), "John Doe", [
    #                                  "Hello World, Motherfucka!", "Like i've ever cared about the world...", "Бля!"],
    #                                                     user_color_real="orange"))
    # Image.open(io.BytesIO(image)).show()

    ## render default avatar with initials
    # avatar_image = Image.new("RGBA", (50, 50))
    # draw_ctx = ImageDraw.Draw(avatar_image)
    # draw_ctx.ellipse((0, 0, 49, 49), (0xff, 0x88, 0x00))
    # user_initials = "".join(map(lambda s: s[:1], ["John", "Doe"])).upper()
    # avatar_font = ImageFont.truetype(ROBOTO_AVATAR_PATH, 25)
    # draw_ctx.text((25, 25), user_initials, fonts.py=avatar_font, anchor="mm")
    # avatar_image.show()

    ## render avatar from image
    avatar_image = Image.open("downloads/photo_2024-07-31_01-01-08_7397552319446908932.jpg")
    avatar_image = ImageOps.fit(avatar_image, (50, 50), method=Image.Resampling.BICUBIC)
    mask = Image.new("L", (100, 100), 0)
    mask_draw_ctx = ImageDraw.Draw(mask)
    mask_draw_ctx.ellipse((0, 0, 99, 99), fill=255)
    mask = mask.resize((50, 50), Image.Resampling.BILINEAR)
    avatar_image.putalpha(mask)
    avatar_image.show()


asyncio.run(main())
