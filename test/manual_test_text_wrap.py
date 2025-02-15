from PIL import Image, ImageDraw, ImageFont

from text import wrap, fonts
import util

def main():
    img = Image.new("RGBA", (300, 400), color=(255, 255, 255, 255))
    font = fonts.OPENSANS_FONT.font_variant(size=25)

    draw = ImageDraw.Draw(img)

    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "\
           "Cras nec ipsum at mi feugiat sollicitudin. Donec et eros nulla. "\
           "Etiam aliquam, leo eget fringilla tristique, libero lorem. "\
           "FSDKFDJFKWIEUFHJDLKSFJSKDLFKSJDKFLSKDNSDJKNLVCKSDJVSKJDLVKSJBDKV"

    wrapped_text, pix_length = wrap.text_wrap(text, font, 300)

    print(wrapped_text)
    print(f"{pix_length} pixels")

    draw.multiline_text((0, 0), "\n".join(wrapped_text), font=font, fill=(0, 0, 255))
    img.show("rendered_text")

if __name__ == "__main__":
    main()