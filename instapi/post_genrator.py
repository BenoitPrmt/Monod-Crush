import textwrap
import time
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# TODO generate url to post dynamically on qr code
# TODO auto change font size
# TODO setup cache


# generate a new image
from instapi.auth import login

IMAGE_SIZE = (1080, 1080)
BACKGROUND_COLOR = "#ff5266"

# logo
LOGO_PATH = "instapi/assets/qr_code.png"
LOGO_SIZE = (200, 200)
LOGO_MARGIN = (20, 20)

# date
DATE_FONT_SIZE = 30
DATE_FONT_PATH = "instapi/assets/Ubuntu-Regular.ttf"
DATE_FORMAT = "%d/%m/%Y"
DATE_MARGIN = (20, 20)
DATE_COLOR = "#ffffff"

# Box
BOX_PADDING = (20, 20)
BOX_BORDER_COLOR = "#a8a09c"
BOX_BORDER_RADIUS = 10
BOX_BORDER_WIDTH = 6
BOX_BACKGROUND_COLOR = "#fff"

# Text
MAX_CHARACTERS_PER_LINE = 45
FONT_COLOR = "#000"
FONT_SIZE = 45
FONT_PATH = "instapi/assets/Oxygen-Regular.ttf"
BORDER_PADDING = 30
BOX_MARGIN = 10

# Footer
FOOTER_TEXT = "monodcrush.fr"
FOOTER_FONT_PATH = "instapi/assets/Ubuntu-Regular.ttf"
FOOTER_FONT_SIZE = 75
FOOTER_BOTTOM_MARGIN = 40
FOOTER_COLOR = "#fff"

# image metadata
TAGS = ["#monodcrush", "#crush", "#lycee", "#monod", "#stjeandebraye", "#sjdb"]
DESCRIPTION = f"Une idée de qui ca peut être ? Met le en commentaire !\n\n{' '.join(TAGS)}"


def generate_pic(text: str) -> Image:
    img = Image.new('RGB', IMAGE_SIZE, color=BACKGROUND_COLOR)

    # paste qr code
    qr_code = Image.open(LOGO_PATH).resize(LOGO_SIZE)
    img.paste(qr_code, LOGO_MARGIN)

    d = ImageDraw.Draw(img)

    # center footer text
    footer_font = ImageFont.truetype(FOOTER_FONT_PATH, FOOTER_FONT_SIZE)
    text_width, text_height = d.textsize(FOOTER_TEXT, font=footer_font)
    text_x = (IMAGE_SIZE[0] - text_width) / 2
    text_y = IMAGE_SIZE[1] - text_height - FOOTER_BOTTOM_MARGIN
    d.text((text_x, text_y), FOOTER_TEXT, fill=FOOTER_COLOR, font=footer_font)

    # date
    date_font = ImageFont.truetype(DATE_FONT_PATH, DATE_FONT_SIZE)
    str_date = date.today().strftime(DATE_FORMAT)
    date_width, date_height = d.textsize(str_date, font=date_font)
    d.text((IMAGE_SIZE[0] - date_width - DATE_MARGIN[0], DATE_MARGIN[1]),
           str_date, fill=DATE_COLOR, font=date_font)

    # prepare text
    lines = textwrap.fill(text, width=MAX_CHARACTERS_PER_LINE)

    main_font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    text_width, text_height = d.textsize(lines, font=main_font)
    text_x = (IMAGE_SIZE[0] - text_width) / 2
    text_y = (IMAGE_SIZE[1] - text_height) / 2

    # Draw box
    d.rounded_rectangle([(text_x - BORDER_PADDING, text_y - BORDER_PADDING),
                         (text_x + text_width + BORDER_PADDING, text_y + text_height + BORDER_PADDING)],
                        radius=BOX_BORDER_RADIUS, outline=BOX_BORDER_COLOR, width=BOX_BORDER_WIDTH,
                        fill=BOX_BACKGROUND_COLOR)

    # draw text
    d.text((text_x, text_y), lines, font=main_font, fill=FONT_COLOR)

    img.save('tmp/test.jpg')

    # send to instagram
    client = login()
    client.photo_upload(Path("tmp/test.jpg"), DESCRIPTION)


if __name__ == '__main__':
    t = time.time()
    generate_pic("test")
    print(time.time() - t)
