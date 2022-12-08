#! /usr/bin/python3

import json
import requests
from inky.inky_uc8159 import Inky
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import datetime
import time
import os, sys
import random

# Get data from config.py file
from config import client_id, client_secret
from config import redirect_uri, refresh_token


scriptdir = sys.path[0]
imagepath = os.path.join(scriptdir, "images")
image_list = os.listdir(imagepath)


def request_token(client_id, client_secret, code):
    print("request_token()")
    response = requests.post(url='https://www.strava.com/oauth/token',
                             data={'client_id': client_id,
                                   'client_secret': client_secret,
                                   'code': code,
                                   'grant_type': 'authorization_code'})
    return response


def get_refresh_token(client_id, client_secret, refresh_token):
    print("refresh_token()")
    tokens = requests.post(url=f'https://www.strava.com/api/v3/oauth/token' \
                               f'?client_id={client_id}' \
                               f'&client_secret={client_secret}' \
                               f'&grant_type=refresh_token' \
                               f'&refresh_token={refresh_token}')

    # Let's save the new token
    strava_tokens = tokens.json()

    with open('strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)


def get_access_token():
    # Read the token from the saved file
    with open('strava_tokens.json', 'r') as tokens:
        data = json.load(tokens)

    # Get the access token
    access_token = data['access_token']
    return access_token


def get_athlete_data(access_token):
    # Build the API url to get athlete info
    athlete_url = f"https://www.strava.com/api/v3/athlete?" \
                  f"access_token={access_token}"

    # # Get the response in json format
    atleteresponse = requests.get(athlete_url)
    athlete = atleteresponse.json()
    return athlete


get_refresh_token(client_id, client_secret, refresh_token)
access_token = get_access_token()
athlete = get_athlete_data(access_token)


# # Print out the retrieved information
print('Name:', athlete['firstname'], '"' + athlete['username'] + '"', athlete['lastname'])
print('ID:', athlete['id'])
athlete_id = athlete['id']



def ride_total_year(access_token):
    stats_url = f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats?" \
                f"access_token={access_token}"

    try:
        statsresponse = requests.get(stats_url)
    except requests.ConnectionError:
        print("ConnectionError")
        exit(1)
    except requests.HTTPError:
        print("HTTPError")
        exit(2)
    except:
        print("Other error")
        exit(3)

    stats = statsresponse.json()
    # print(stats)

    print('Stats API:', stats_url)
    ride_total_year = round(stats['ytd_ride_totals']['distance']/1000,1 )
    print(f"biggest_ride_distance: {stats['biggest_ride_distance']/1000} km")
    print(f"ytd_ride_totals distance: {ride_total_year} km")
    return(ride_total_year)


def ride_total_month(access_token):
    now = datetime.datetime.today()
    # Get the first day of this month (so we can query from the start of this)
    firstday = now.replace(day=1)
    firstday_epoch = datetime.datetime(now.year, now.month, firstday.day).timestamp()
    print(f"firstday_epoch: {firstday_epoch}")

    activities_url = f"https://www.strava.com/api/v3/athlete/activities?" \
                    f"access_token={access_token}" \
                    f"&after={firstday_epoch}"

    print('Activities API:', activities_url)

    try:
        activitiesresponse = requests.get(activities_url)
    # except requests.ConnectionError:
    #     print("ConnectionError")
    #     exit(1)
    except requests.HTTPError:
        print("HTTPError")
        exit(2)
    except requests.AuthorizationError:
        print("AuthorizationError")
        exit(3)
    except:
        print("Other error")
        exit(4)

    activities = activitiesresponse.json()
    print(activities)

    # Filter on rides
    rides = [x for x in activities if x['sport_type'] == 'Ride']

    sum_ride_m = 0
    for ride in rides:
        # print(f"activity: {activity}")
        print(f"Name: {ride['name']}")
        print(f"sport_type: {ride['sport_type']}")
        # print(f"workout_type: {ride['workout_type']}")
        print(f"Date: {ride['start_date']}")
        print(f"Distance: {ride['distance']} m")
        sum_ride_m += ride['distance']
        # print(f"Average Speed: {activity['average_speed']} m/s")
        # print(f"Max Speed: {activity['max_speed']} m/s")

    
    return round(sum_ride_m/1000,1)


rideyeartotal = ride_total_year(access_token)
ridemonthtotal = ride_total_month(access_token)
print(f"Kms this year: {rideyeartotal}")
print(f"Kms this month: {ridemonthtotal}")



inky_display = Inky()
inky_display.set_border(inky_display.BLACK)

img = Image.new("P", (600, 448))

# Pick a random image from the list of files in the images directory
randomimage = random.choice(image_list)
backgroundimage = os.path.join(imagepath, randomimage)
bikeinwoodsimg = Image.open(backgroundimage, "r")
bikeinwoodsimg_w, bikeinwoodsimg_h = bikeinwoodsimg.size

# Bicycle icon
back_im = img.copy()
# bikeimage_position = (25, 25)
back_im.paste(bikeinwoodsimg, (0,0))
# back_im.paste(bikeimg, (25, round((inky_display.HEIGHT / 2) - (h / 2) - 100 - bikeimg_h/2)))


draw = ImageDraw.Draw(img)
largefont = ImageFont.truetype("usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 50)
font = ImageFont.truetype("usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 24)
smallfont = ImageFont.truetype("usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 18)

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

messageyear = f"{rideyeartotal} km"
yeardescription = "distance this year"
w, h = font.getsize(messageyear)
yeardesc_position = (120, 40)
year_position = (220, 90)

messagemonth = f"{ridemonthtotal} km"
monthdescription = "distance this month"
monthtext_width, monthtext_height = font.getsize(messagemonth)
monthdesc_position = (120, 160)
month_position = (250, 200)

# Extrapolation kms this year:
date = datetime.date.today()
daystoday = (datetime.datetime.now().timestamp()-time.mktime(datetime.date(year=date.year, month=1, day=1).timetuple()))/60/60/24
# To solve: on 1 jan daystoday will be 0. Division by 0.
extrapol_yeartotal = round(rideyeartotal * (365/daystoday),1)
messageexpy = f"{extrapol_yeartotal} km"
yearextrapol_description = "projected kms this year"
yearextrapoldesc_position = (120, 270)
yearextrapol_position = (220, 310)

with Image.open(backgroundimage) as img:

    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox(year_position, messageyear, font=font)
    # draw.rectangle((0, 0, inky_display.WIDTH, inky_display.HEIGHT), fill=inky_display.WHITE)
    draw.text(yeardesc_position, yeardescription, year_fill, font, stroke_width=description_stroke, stroke_fill=year_shadow)
    draw.text(year_position, messageyear, year_fill, largefont, stroke_width=message_stroke, stroke_fill=year_shadow)
    draw.text(monthdesc_position, monthdescription, month_fill, font, stroke_width=description_stroke, stroke_fill=month_shadow)
    draw.text(month_position, messagemonth, month_fill, largefont, stroke_width=message_stroke, stroke_fill=month_shadow)
    draw.text(yearextrapoldesc_position, yearextrapol_description, yearextrapol_fill, font, stroke_width=description_stroke, stroke_fill=yearextrapol_shadow)
    draw.text(yearextrapol_position, messageexpy, yearextrapol_fill, largefont, stroke_width=message_stroke, stroke_fill=yearextrapol_shadow)


    # Last update
    now = datetime.datetime.today()
    lastupdate = f"Last update: {now.year}-{now.month}-{now.day} {now.hour}:{now.minute}"
    lastupdate_width, lastupdate_height = font.getsize(lastupdate)
    lastupdate_position = ((inky_display.WIDTH / 2) - (lastupdate_width / 2) + 150, \
                    (inky_display.HEIGHT / 2) - (lastupdate_height) + 210)
    draw.text(lastupdate_position, lastupdate, inky_display.BLACK, smallfont)

# Image out to test if colours display differently on the Inky display
img.save("stravainky_dashboard_out.png")

inky_display.set_image(img)
inky_display.show()
