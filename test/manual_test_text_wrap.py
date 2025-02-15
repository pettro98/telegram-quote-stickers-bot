from PIL import Image, ImageDraw

from text import wrap, fonts

# Test for text-wrap function which uses Unicode text-wrapping algorithm
# Variables for manual testing:
# - font: any PIL.ImageFont.FreeTypeFont object with set parameters
# - text: any SINGLE line of text, which SHOULD have at least one very-long-word to test grapheme-breaking algorithm
# - canvas_size: (width_px, height_px) tuple which is used for canvas creation
# - text_guides: (left_px, right_px) offsets of ruler-guides between which all text should be rendered
# Result:
# - text MUST be correctly rendered and broken into lines (very-long-words should break between whole graphemes)
# - rendered glyphs MUST NOT be cut off by left or right ruler guide
def main():
    font = fonts.OPENSANS_FONT.font_variant(size=25)

    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "\
           "Cras nec ipsum at mi feugiat sollicitudin. Donec et eros nulla. "\
           "Etiam aliquam, leo eget fringilla tristique, libero lorem. "\
           "FSDKFDJFKWIEUFHJDLKSFJSKDLFKSJDKFLSKDNSDJKNLVCKSDJVSKJDLVKSJBDKV"

    canvas_size = (300, 500)
    text_guides = (20, 280)


    wrapped_text, text_width = wrap.text_wrap(text, font, text_guides[1] - text_guides[0])

    print(f"Wrapped text:\n{"\n".join(wrapped_text)}")
    print(f"Text area width: {text_guides[1] - text_guides[0]} px")
    print(f"Max rendered text width: {text_width} px")

    img = Image.new("RGBA", canvas_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # draw guides
    draw.line((text_guides[0], 0, text_guides[0], canvas_size[1]), fill=(255, 0, 0))
    draw.line((text_guides[1], 0, text_guides[1], canvas_size[1]), fill=(255, 0, 0))

    # draw text
    draw.multiline_text((text_guides[0], 0), "\n".join(wrapped_text), font=font, fill=(0, 0, 0))

    img.show("rendered_text")

if __name__ == "__main__":
    main()