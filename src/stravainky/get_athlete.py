#! /usr/bin/python3
"""
stravainky_dashboard.py

Displaying Strava stats on a Inky Impressions e-ink display
"""
import os
from dotenv import load_dotenv
import logging
import json
from stravalib import Client
from strava_access import get_strava_token, get_strava_client


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

logger.info('Start of get_athlete.py')
logger.info('====================================')


# Get the current athlete's details
def get_athlete_data(strava_client):
    """ Get the current athlete's details.

    Args:
        strava_client (Client): The Strava client instance.

    Returns:
        Athlete: The athlete's details.
    """
    # Create a Strava client
    athlete = strava_client.get_athlete()  # Get current athlete details
    logger.info(f"Retrieving data for athlete {athlete.firstname} {athlete.lastname}")
    logger.debug(f"Athlete data: {athlete}")
    return athlete
