from PIL import Image, ImageDraw, ImageFont
import os

import text_fit

def get_project_abspath(relative: str):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", relative))


def main():
    img = Image.new("RGBA", (300, 400), color=(255, 255, 255, 255))
    font = ImageFont.truetype(get_project_abspath("assets/Roboto-Medium.ttf"), 25)

    draw = ImageDraw.Draw(img)

    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "\
           "Cras nec ipsum at mi feugiat sollicitudin. Donec et eros nulla. "\
           "Etiam aliquam, leo eget fringilla tristique, libero lorem. "\
           "FSDKFDJFKWIEUFHJDLKSFJSKDLFKSJDKFLSKDNSDJKNLVCKSDJVSKJDLVKSJBDKV"

    wrapped_text, pix_length = text_fit.text_width_fit(text, font, 300)

    print(wrapped_text)
    print(f"{pix_length} pixels")

    draw.multiline_text((0, 0), "\n".join(wrapped_text), font=font, fill=(0, 0, 255))
    img.show("rendered_text")

if __name__ == "__main__":
    main()