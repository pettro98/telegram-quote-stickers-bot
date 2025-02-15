from dataclasses import dataclass


@dataclass
class UserSettings:
    _VERSION: int = 1
    outline_color: str = "white"
    outline_width: str = "2px"
    background_color: str = "#24303f"  # got from Telegram default dark mode on macOS
    text_color: str = "#f8f8f8"  # got from Telegram default dark mode on macOS
    font_size: int = 24
    username_color: str = "auto"  # get color from Telegram APIs or use default
