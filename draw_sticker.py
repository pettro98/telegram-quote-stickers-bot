import time

import pyrogram as pg
import pyrogram.types as pg_t
import user_db
from bot_utils import get_project_abspath
import pyppeteer
import jinja2
import base64
import io
from PIL import Image, ImageFont, ImageOps, ImageDraw
from dataclasses import dataclass, asdict
from bot_utils import timed_zone

_ROBOTO_REGULAR_PATH = get_project_abspath("assets/Roboto-Regular.ttf")
_ROBOTO_ITALIC_PATH = get_project_abspath("assets/Roboto-Italic.ttf")
_ROBOTO_MEDIUM_REGULAR_PATH = get_project_abspath("assets/Roboto-Bold.ttf")
_ROBOTO_MEDIUM_ITALIC_PATH = get_project_abspath("assets/Roboto-BoldItalic.ttf")


@dataclass
class PrivateDrawingSettings:
    avatar_mime: str
    avatar_data: bytes
    user_name: list[str]
    messages: list[str]
    user_color_real: str


# TODO: test with emojis in text/user name
# TODO: merge style and message configs (make a dataclass?)
async def render_sticker(browser: pyppeteer.launcher.Browser, render_env: jinja2.Environment,
                         user_settings: user_db.UserDrawingSettings,
                         private_settings: PrivateDrawingSettings):
    avatar_data_encoded = base64.b64encode(private_settings.avatar_data).decode("ascii")
    font_data_b64: str
    with open(_ROBOTO_REGULAR_PATH, "rb") as font_file:
        font_data_b64 = base64.b64encode(font_file.read()).decode("ascii")

    initials = map(lambda s: s[:1], private_settings.user_name)
    html_data = render_env.get_template("sticker_template.html.jinja").render(**asdict(user_settings),
                                                                              **asdict(private_settings),
                                                                              avatar_data_b64=avatar_data_encoded,
                                                                              initials=initials,
                                                                              font_data_b64=font_data_b64)
    encoded_html_data = base64.b64encode(html_data.encode("utf-8")).decode("ascii")
    page = await browser.newPage()
    await page.goto(f"data:text/html;base64,{encoded_html_data}")
    body_el = await page.querySelector("body")
    img_data = io.BytesIO()
    Image.open(io.BytesIO(await body_el.screenshot({"omitBackground": True}))).save(img_data, "webp")
    await page.close()
    return img_data.getvalue()


# TODO add outline?
async def pillow_render_sticker(_, __, user_settings: user_db.UserDrawingSettings,
                                private_settings: PrivateDrawingSettings):
    # render avatar to image
    if private_settings.avatar_data is None:
        avatar_image = Image.new("RGBA", (50, 50))
        draw_ctx = ImageDraw.Draw(avatar_image)
        draw_ctx.ellipse((0, 0, 49, 49), private_settings.user_color_real)  # format rgb(int, int, int)
        user_initials = "".join(map(lambda s: s[:1], private_settings.user_name)).upper()
        avatar_font = ImageFont.truetype(_ROBOTO_MEDIUM_REGULAR_PATH, 25)
        draw_ctx.text((25, 25), user_initials, font=avatar_font, anchor="mm", fill="white")
    else:
        avatar_image = Image.open(io.BytesIO(private_settings.avatar_data))
        avatar_image = ImageOps.fit(avatar_image, (50, 50), method=Image.Resampling.BICUBIC)
        mask = Image.new("L", (100, 100), 0)
        mask_draw_ctx = ImageDraw.Draw(mask)
        mask_draw_ctx.ellipse((0, 0, 99, 99), fill=255)
        mask = mask.resize((50, 50), Image.Resampling.BILINEAR)
        avatar_image.putalpha(mask)

    # sticker height = 2 * message_padding + N * line_height
    # N is message lines count +1 for user name
    # max line length is avatar_width + margin +
    # so lets count lines by recomputing text bounding box by adding words
    message_font = ImageFont.truetype(_ROBOTO_MEDIUM_REGULAR_PATH, 20)

    sticker_image = Image.new("RGBA", (512, 512))
