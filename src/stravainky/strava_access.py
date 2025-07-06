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


# Load the environment variables
load_dotenv()

STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
STRAVA_ACCESS_TOKEN = os.environ.get("STRAVA_ACCESS_TOKEN")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

logger.info('Start of strava_access.py')
logger.info('====================================')


def get_strava_token(strava_token_file="strava_tokens.json"):
    """ get_strava_tokens

    Args:
        strava_tokens_file (str, optional): _description_. Defaults to "strava_tokens.json".
    
    Returns:
        dict: A dictionary containing the Strava access token, refresh token, and expiration time.
    """
    json_path = os.path.join(strava_token_file)
    # Read the JSON file containing the Strava tokens
    if not os.path.exists(json_path):
        logger.error(f"Token file {json_path} does not exist.")
        raise FileNotFoundError(f"Token file {json_path} does not exist.")
    else:
        with open(json_path, "r") as f:
            token_refresh = json.load(f)
        logger.info(f"Stored token expires at: {token_refresh['expires_at']}")
        return token_refresh


def get_strava_client(stored_token="strava_tokens.json"):
    """
    Returns a Strava Client instance with the access token.

    Args:
        stored_token (str): Path to the JSON file containing the Strava tokens.

    Returns:
        Client: A Strava Client instance initialized with the access token.

    """
    client = Client(
        access_token=stored_token["access_token"],
        refresh_token=stored_token["refresh_token"],
        token_expires=stored_token["expires_at"],
    )
    logger.info(f"Token expires at: {client.token_expires}")
    return client
