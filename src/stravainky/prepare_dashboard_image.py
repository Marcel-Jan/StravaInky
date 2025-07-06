""" This script prepares a dashboard image by processing a given image file.
"""
import os
import random
import logging
import datetime
from PIL import Image, ImageFont, ImageDraw


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

logger.info('Start of prepare_dashboard_image.py')
logger.info('====================================')


def pick_image(scriptdir):
    """ Pick a random image from the image directory

    Args:
        scriptdir (str): directory from where the script is run

    Returns:
        ospath: location of the image
    """
    imagepath = os.path.join(scriptdir, "images")
    image_list = os.listdir(imagepath)
    randomimage = random.choice(image_list)
    backgroundimage = os.path.join(imagepath, randomimage)
    return backgroundimage


def prepare_dashboard_image(ridekmyear, ridekmmonth, ridekmyearextrapol, image_width, image_height, font_name, scriptdir):
    """ Prepare the dashboard image by copying the image file to the images directory

    Args:
        ridekmyear (float): distance ridden this year in km
        ridekmmonth (float): distance ridden this month in km
        ridekmyearextrapol (float): extrapolated distance for the year in km
        image_width (int): width of the image in pixels
        image_height (int): height of the image in pixels
        scriptdir (str): directory from where the script is run

    Returns:
        ospath: location of the copied image
    """
    imagepath = os.path.join(scriptdir, "images")
    if not os.path.exists(imagepath):
        os.makedirs(imagepath)

    backgroundimage = pick_image(scriptdir)
    background = os.path.join(scriptdir, "images", backgroundimage)
    if not os.path.exists(background):
        raise FileNotFoundError(f"Background image file {background} does not exist.")

    display_width = image_width
    display_height = image_height

    # Open the background image and resize it to the display dimensions
    logger.info(f"Opening background image: {backgroundimage}")
    dashboard_image = Image.open(backgroundimage, "r").resize((display_width, display_height))

    # Resize the image to fit the display dimensions
    draw = ImageDraw.Draw(dashboard_image)

    largefont = ImageFont.truetype("usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 50)
    font = ImageFont.truetype("usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 24)
    smallfont = ImageFont.truetype("usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 18)

    # Large font on Mac
    # largefont = ImageFont.truetype(font_name, 50)
    # font = ImageFont.truetype(font_name, 24)
    # smallfont = ImageFont.truetype(font_name, 18)

    # Get size of the fonts without AttributeError object has no attribute 'getsize'
    largefont_bbox = largefont.getbbox("0")
    largefont_width = largefont_bbox[2] - largefont_bbox[0]
    largefont_height = largefont_bbox[3] - largefont_bbox[1]
    font_bbox = font.getbbox("0")
    font_width = font_bbox[2] - font_bbox[0]
    font_height = font_bbox[3] - font_bbox[1]
    smallfont_bbox = smallfont.getbbox("0")
    smallfont_width = smallfont_bbox[2] - smallfont_bbox[0]
    smallfont_height = smallfont_bbox[3] - smallfont_bbox[1]
 
    logger.debug(f"Large font size: {largefont_width}x{largefont_height}")
    logger.debug(f"Font size: {font_width}x{font_height}")
    logger.debug(f"Small font size: {smallfont_width}x{smallfont_height}")


    # Text colours
    year_fill = "blue"
    year_shadow = "white"
    month_fill = "red"
    month_shadow = "white"
    yearextrapol_fill = "green"
    yearextrapol_shadow = "white"
    # Text outline settings
    message_stroke = 4
    description_stroke = 2

    # Text positions and descriptions for year, month, and extrapolated year
    messageyear = f"{ridekmyear:.1f} km"
    yeardescription = "distance this year"
    yeardesc_position = (120, 40)
    year_position = (220, 90)

    messagemonth = f"{ridekmmonth:.1f} km"
    monthdescription = "distance this month"
    monthdesc_position = (120, 160)
    month_position = (250, 200)

    messageexpy = f"{ridekmyearextrapol:.1f} km"
    yearextrapol_description = "projected kms this year"
    yearextrapoldesc_position = (120, 270)
    yearextrapol_position = (220, 310)

    # Draw the text on the image
    draw.text(yeardesc_position, yeardescription, year_fill, font, 
                stroke_width=description_stroke, stroke_fill=year_shadow)
    draw.text(year_position, messageyear, year_fill, largefont, 
                stroke_width=message_stroke, stroke_fill=year_shadow)
    draw.text(monthdesc_position, monthdescription, month_fill, font, 
                stroke_width=description_stroke, stroke_fill=month_shadow)
    draw.text(month_position, messagemonth, month_fill, largefont, 
                stroke_width=message_stroke, stroke_fill=month_shadow)
    draw.text(yearextrapoldesc_position, yearextrapol_description, 
                yearextrapol_fill, font, stroke_width=description_stroke, 
                stroke_fill=yearextrapol_shadow)
    draw.text(yearextrapol_position, messageexpy, yearextrapol_fill, 
                largefont, stroke_width=message_stroke, 
                stroke_fill=yearextrapol_shadow)


    # Last update
    now = datetime.datetime.today()
    # Show last update time in the format "Last update: YYYY-MM-DD HH:MM"
    lastupdate = f"Last update: {now.strftime('%Y-%m-%d %H:%M')}"
    logger.info(f"Last update: {lastupdate}")

    # Position the last update text in the center of the display
    lastupdate_position = ((display_width / 2) - (largefont_width / 2) + 50, \
                    (display_height / 2) - (largefont_height) + 210)
    black = (0, 0, 0)

    # Draw white background rectangle for last update text
    lastupdate_bbox = draw.textbbox(lastupdate_position, lastupdate, smallfont)
    draw.rectangle(lastupdate_bbox, fill="white")
    draw.text(lastupdate_position, lastupdate, black, smallfont)

    return dashboard_image

