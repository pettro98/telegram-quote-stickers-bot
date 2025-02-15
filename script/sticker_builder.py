import io
import base64
import os


# for some reason the default hardcoded Chromium version in puppeteer is unavailable to download for windows
# as of 15 feb 2025 the  issue is still there (see https://github.com/pyppeteer/pyppeteer/issues/483)
# variable needs to be set before importing pyppeteer
os.environ["PYPPETEER_CHROMIUM_REVISION"] = "1181217"


from PIL import Image, ImageDraw, ImageFont, ImageOps
import pyppeteer
import jinja2

import util
from text import fonts



class StickerBuilder:
    def __init__(self):
        self.messages: list[str] = []
        self.avatar: Image = None
        self.nickname: str = None
        self.initials: str = None
        self.background: tuple[int, int, int] = (0, 0, 0)  # RGB
        self.accent: tuple[int, int, int] = (0, 0, 0)  # RGB of avatar background and nickname
        self.text_color: tuple[int, int, int] = (0, 0, 0)  # RGB

    def add_message(self, text: str):
        self.messages.append(text)
        return self

    def set_avatar(self, avatar: Image):
        self.avatar = avatar
        return self

    def set_nickname(self, nickname: str):
        self.nickname = nickname
        split_name = nickname.split()
        if len(split_name) == 0:
            self.initials = ""
        else:
            self.initials = split_name[0][0]
            if len(split_name) > 1:
                self.initials += split_name[-1][0]
                self.initials = self.initials.upper()

    def set_background(self, color: tuple[int, int, int]):
        self.background = color
        return self

    def set_accent(self, color: tuple[int, int, int]):
        self.accent = color
        return self

    def set_text_color(self, color: tuple[int, int, int]):
        self.text_color = color
        return self

    async def build(self):
        assert self.nickname is not None, "Nickname must be set"
        assert len(self.messages) != 0, "Messages must be set"

        if self.avatar is not None:
            self.avatar = ImageOps.fit(self.avatar, (50, 50), method=Image.Resampling.BICUBIC)
        else:
            avatar_image = Image.new("RGBA", (50, 50))
            draw_ctx = ImageDraw.Draw(avatar_image)
            draw_ctx.ellipse((0, 0, 49, 49), self.accent)
            avatar_font = fonts.OPENSANS_FONT.font_variant(size=25)
            draw_ctx.text((25, 25), self.initials, font=avatar_font, anchor="mm", fill=(255, 255, 255))
            self.avatar = avatar_image

        avatar_io = io.BytesIO()
        self.avatar.save(avatar_io, "PNG")

        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(util.get_project_abspath("assets")), undefined=jinja2.StrictUndefined)

        font_data_b64 = fonts.OPENSANS_FONT_B64

        template_params = dict(
            font_data_b64=font_data_b64,
            user_color_real=f"#{self.accent[0]:02x}{self.accent[1]:02x}{self.accent[2]:02x}",
            outline_width="0px",
            outline_color="#0000",
            background_color=f"#{self.background[0]:02x}{self.background[1]:02x}{self.background[2]:02x}",
            text_color=f"#{self.text_color[0]:02x}{self.text_color[1]:02x}{self.text_color[2]:02x}",
            font_size=24,
            initials=self.initials,
            avatar_data_b64=base64.b64encode(avatar_io.getvalue()).decode("ascii"),
            avatar_mime="image/png",
            user_name=self.nickname,
            messages=self.messages,
        )

        html_data = jinja_env.get_template("sticker_template.html.jinja").render(template_params)
        encoded_html_data = base64.b64encode(html_data.encode("utf-8")).decode("ascii")

        browser = await pyppeteer.launch(headless=True, autoClose=True)
        page = await browser.newPage()
        await page.goto(f"data:text/html;base64,{encoded_html_data}")
        body_el = await page.querySelector("body")
        img_data = io.BytesIO()
        Image.open(io.BytesIO(await body_el.screenshot({"omitBackground": True}))).save(img_data, "webp")
        await page.close()
        await browser.close()
        return img_data.getvalue()
