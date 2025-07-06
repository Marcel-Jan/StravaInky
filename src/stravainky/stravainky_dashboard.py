#! /usr/bin/python3
"""
stravainky_dashboard.py

Displaying Strava stats on a Inky Impressions e-ink display
"""
import os
from dotenv import load_dotenv
import logging
from PIL import Image, ImageDraw, ImageFont
from stravalib import Client
from get_athlete import get_athlete_data
from strava_access import get_strava_token, get_strava_client
from get_strava_data import stats_to_display, get_activities
from prepare_dashboard_image import prepare_dashboard_image


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

logger.info('Start of stravainky_dashboard.py')
logger.info('====================================')

load_dotenv()  # Load environment variables from .env file

# Current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
logging.info(f"Current directory: {current_dir}")

# Read strava_tokens.json from the current directory
STRAVA_TOKEN_FILE = os.path.join(current_dir, "strava_tokens.json")


def inky_get_display_size():
    """ Get the display size of the Inky Impressions e-ink display

    Returns:
        tuple: Width and height of the display (pixels)
    """
    from inky import InkyPHAT  # Import here to avoid dependency issues if not using Inky display
    from inky.auto import auto
    inky_display = auto()
    return inky_display.WIDTH, inky_display.HEIGHT


def inky_display_image(image):
    """ Display the image on the Inky Impressions e-ink display

    Args:
        image (PIL.Image): The image to display
    """
    from inky import InkyPHAT  # Import here to avoid dependency issues if not using Inky display
    from inky.auto import auto
    inky_display = auto()
    inky_display.set_border(inky_display.BLACK)  # Set border color
    inky_display.set_image(image)  # Set the image to be displayed
    inky_display.show()  # Show the image on the display
    logger.info("Image displayed on Inky Impressions e-ink display")


def main():
    logging.info(f"strava token file: {STRAVA_TOKEN_FILE}")
    # Create a Strava client
    client = get_strava_client(get_strava_token(STRAVA_TOKEN_FILE))  # Get Strava client with access token

    # Get the current athlete's details
    athlete = get_athlete_data(client)  # Get current athlete details
    logger.info(f"Retrieving data for athlete {athlete.firstname} {athlete.lastname}")

    activities = get_activities(client)  # Get the latest activities of the athlete

    # Get the athlete's stats
    rideyeartotal, ridemonthtotal, extrapol_yeartotal = stats_to_display(client, activities)
    logger.info(f"Athlete stats: {rideyeartotal} km this year, {ridemonthtotal} km this month, extrapolated {extrapol_yeartotal} km for the year")
    
    # Chec if the Inky Impressions display is available
    try:
        display_width, display_height = inky_get_display_size()
        logger.info(f"Inky Impressions display size: {display_width}x{display_height}")
        font_name = "usr/share/fonts/truetype/noto/NotoMono-Regular.ttf"  # Font for the dashboard
    except ImportError:
        logger.warning("Inky Impressions display not available. Skipping display step.")
        display_width, display_height = 600, 448  # Default size for non-Inky displays
        font_name = "Arial.ttf"  # Fallback font for non-Inky displays

    # Prepare the dashboard image with the athlete's data
    rootdir = os.path.dirname(os.path.abspath(__file__))
    scriptdir = os.path.dirname(os.path.dirname(rootdir))

    prepared_image = prepare_dashboard_image(rideyeartotal, ridemonthtotal, extrapol_yeartotal, 
                                             display_width, display_height, font_name, scriptdir)
    
    # Save or display the prepared image as needed
    prepared_image.save("stravainky_dashboard_out.png")
    
    try:
        inky_display_image(prepared_image)  # Display the image on the Inky Impressions e-ink display
        logger.info("Dashboard image prepared and displayed successfully.")
    except ImportError:
        logger.warning("Inky Impressions display not available or inky package not installed. Skipping display step.")
    logger.info("Dashboard image prepared successfully.")

if __name__ == '__main__':
    main()
