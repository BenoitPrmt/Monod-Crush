import logging
import os
import textwrap
from datetime import date

from PIL import Image, ImageDraw, ImageFont
from settings import INSTA_USERNAME, INSTA_PASSWORD
from instagrapi import Client

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def login() -> Client:
    cl = Client()
    if not os.path.exists("tmp/dump.json"):
        # create a new file and directory
        log.info("Creating new dump.json file")
        os.makedirs("tmp", exist_ok=True)
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)
        cl.dump_settings('tmp/dump.json')
    else:
        log.info("Loading dump.json file")
        cl.load_settings("tmp/dump.json")
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)
        cl.get_timeline_feed()  # check session
    return cl


# TODO generate url to post dynamically
# TODO auto change font size


# generate a new image
IMAGE_SIZE = (1080, 1080)
BACKGROUND_COLOR = "#ff5265"

# logo
LOGO_PATH = "flaskr/assets/qr_code.png"
LOGO_SIZE = (150, 150)
LOGO_MARGIN = (20, 20)

# date
DATE_FONT_SIZE = 40
DATE_FONT_PATH = "flaskr/assets/Ubuntu-Regular.ttf"
DATE_FORMAT = "%d/%m/%Y"
DATE_MARGIN = (40, 50)
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
FONT_PATH = "flaskr/assets/Oxygen-Regular.ttf"
BORDER_PADDING = 30
BOX_MARGIN = 10

# Footer
FOOTER_TEXT = "monodcrush.fr"
FOOTER_FONT_PATH = "flaskr/assets/Oxygen-Bold.ttf"
FOOTER_FONT_SIZE = 60
FOOTER_BOTTOM_MARGIN = 50
FOOTER_COLOR = "#fff"

# image metadata
TAGS = ["#monodcrush", "#crush", "#lycee", "#monod", "#stjeandebraye", "#sjdb"]


def generate_pic(text: str) -> Image:
    img = Image.new('RGB', IMAGE_SIZE, color=BACKGROUND_COLOR)

    # paste qr code
    qr_code = Image.open(LOGO_PATH)
    qr_code = qr_code.resize(LOGO_SIZE)
    img.paste(qr_code, LOGO_MARGIN)

    d = ImageDraw.Draw(img)

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

    # center footer text
    footer_font = ImageFont.truetype(FOOTER_FONT_PATH, FOOTER_FONT_SIZE)
    text_width, text_height = d.textsize(FOOTER_TEXT, font=footer_font)
    assert text_width < IMAGE_SIZE[0]
    text_x = (IMAGE_SIZE[0] - text_width) / 2
    text_y = IMAGE_SIZE[1] - text_height - FOOTER_BOTTOM_MARGIN
    d.text((text_x, text_y), FOOTER_TEXT, fill=FOOTER_COLOR, font=footer_font)

    img.save('tmp/test.jpg', quality=100)

    # send to instagram
    client = login()
    client.photo_upload("tmp/test.jpg", f"Une idée de qui ca peut être ? Met le en commentaire !\n\n{' '.join(TAGS)}")