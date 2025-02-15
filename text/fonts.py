import base64
import pathlib

from PIL import ImageFont

import util

_OPENSANS_FONT_PATH = util.get_project_abspath("assets/OpenSans-VariableFont_wdth,wght.ttf")
_OPENSANS_ITALIC_FONT_PATH = util.get_project_abspath("assets/OpenSans-Italic-VariableFont_wdth,wght.ttf")

OPENSANS_FONT = ImageFont.truetype(_OPENSANS_FONT_PATH)
OPENSANS_ITALIC_FONT = ImageFont.truetype(_OPENSANS_ITALIC_FONT_PATH)

OPENSANS_FONT_B64 = base64.b64encode(pathlib.Path(_OPENSANS_FONT_PATH).read_bytes()).decode("ascii")
OPENSANS_ITALIC_FONT_B64 = base64.b64encode(pathlib.Path(_OPENSANS_ITALIC_FONT_PATH).read_bytes()).decode("ascii")


_ROBOTO_FONT_PATH = util.get_project_abspath("assets/Roboto-VariableFont_wdth,wght.ttf")
_ROBOTO_ITALIC_FONT_PATH = util.get_project_abspath("assets/Roboto-Italic-VariableFont_wdth,wght.ttf")

ROBOTO_FONT = ImageFont.truetype(_ROBOTO_FONT_PATH)
ROBOTO_ITALIC_FONT = ImageFont.truetype(_ROBOTO_ITALIC_FONT_PATH)

ROBOTO_FONT_B64 = base64.b64encode(pathlib.Path(_ROBOTO_FONT_PATH).read_bytes()).decode("ascii")
ROBOTO_ITALIC_FONT_B64 = base64.b64encode(pathlib.Path(_ROBOTO_ITALIC_FONT_PATH).read_bytes()).decode("ascii")
