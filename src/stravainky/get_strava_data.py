#! /usr/bin/python3
"""
Get Strava athlete data

"""
import os
from dotenv import load_dotenv
import logging
import datetime
import calendar
from strava_access import get_strava_token, get_strava_client


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

logger.info('Start of get_athlete.py')
logger.info('====================================')


# Get the current athlete's details
def get_athlete_data(strava_client):
    athlete = strava_client.get_athlete()  # Get current athlete details
    logger.info(f"Retrieving data for athlete {athlete.firstname} {athlete.lastname}")
    logger.debug(f"Athlete data: {athlete}")
    
    return athlete


def get_athlete_stats(strava_client):
    """
    Get the athlete's stats.
    
    Args:
        strava_client (Client): The Strava client instance.
    
    Returns:
        AthleteStats: The athlete's stats.
    """
    logger.info(f"Running get_athlete_stats()")
    stats = strava_client.get_athlete_stats()
    logger.debug(f"Athlete stats: {stats}")
    
    return stats


def get_activities(strava_client):
    """
    Get the latest activities of the athlete.
    
    Args:
        strava_client (Client): The Strava client instance.
    
    Returns:
        list: A list of activities.
    """
    logger.info(f"Running get_activities()")
    first_day_of_month = datetime.datetime.now().replace(day=1).strftime("%Y-%m-%d")
    logger.info(f"Retrieving activities after {first_day_of_month}")
    activities = strava_client.get_activities(after=first_day_of_month)
    # logger.info(f"Retrieved {len(activities)} activities.")
    logger.debug(f"Activities: {activities}")
    return activities


def rides_total_month(activities):
    """
    Calculate the total distance of rides for the current month.
    
    Args:
        activities (list): List of activities.
    
    Returns:
        float: Total distance of rides in meters.
    """
    total_distance = 0.0
    
    for activity in activities:
        if activity.sport_type == 'Ride':
            total_distance += activity.distance
    
    logger.info(f"Total distance of rides this month: {total_distance} meters")
    return total_distance


def stats_to_display(client, activities):
    """ stats_to_display

    Args:
        strava_client (Client): The Strava client instance.
        activities (list): List of activities.

    Returns:
        tuple: A tuple containing the total distance of rides this year, this month, and extrapolated to the end of the year.
    """
    athlete = get_athlete_data(client)
    stats = get_athlete_stats(client)
    activities = get_activities(client)
    
    # Example output
    logger.info(f"Athlete: {athlete.firstname} {athlete.lastname}")

    # Ride kms this year
    rideyeartotal = stats.ytd_ride_totals.distance / 1000
    logger.info(f"Ride kms this year: {rideyeartotal:.2f} km")

    # Ride kms this month
    ridemonthtotal = rides_total_month(activities) / 1000
    logger.info(f"Total distance of rides this month: {ridemonthtotal:.2f} km")

    # Extrapolate the total distance to end of this year based on ytd_ride_totals
    year = datetime.datetime.now().year
    days_in_year = 365 + calendar.isleap(year)
    days_passed = (datetime.datetime.now() - datetime.datetime(datetime.datetime.now().year, 1, 1)).days
    extrapol_yeartotal = (stats.ytd_ride_totals.distance / days_passed) * days_in_year / 1000
    logger.info(f"Days passed this year: {days_passed}")
    logger.info(f"Total distance extrapolated to end of year: {extrapol_yeartotal:.2f} km")

    return rideyeartotal, ridemonthtotal, extrapol_yeartotal


