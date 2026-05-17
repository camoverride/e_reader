import time
import textwrap

from PIL import Image, ImageDraw, ImageFont

# E-paper driver
from waveshare_epd import epd1in54_V2


# ----------------------------
# LOAD BOOK TEXT
# ----------------------------

with open("book.txt", "r") as f:
    text = f.read()

position = 0


# ----------------------------
# SET UP DISPLAY
# ----------------------------

epd = epd1in54_V2.EPD()

epd.init()
epd.Clear(0xFF)

WIDTH = epd.height
HEIGHT = epd.width

image = Image.new("1", (WIDTH, HEIGHT), 255)

draw = ImageDraw.Draw(image)

font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    18
)


# ----------------------------
# MAIN LOOP
# ----------------------------

while True:

    # Get next chunk of text
    page = text[position:position + 220]

    # Restart at beginning
    if not page:
        position = 0
        continue

    # Clear screen
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=255)

    # Wrap text
    wrapped = textwrap.fill(page, width=22)

    # Draw text
    draw.text((5, 5), wrapped, font=font, fill=0)

    # Update display
    epd.display(epd.getbuffer(image))

    # Move forward in text
    position += 220

    # Wait 5 seconds
    time.sleep(5)