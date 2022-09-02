# import libraries

import requests
import json
import datetime
import pywhatkit

from datetime import timedelta
import time

# Bootstrap by getting the most recent time that had minutes as a multiple of 5
time_now = datetime.datetime.now()  # Or .now() for local time
prev_minute = time_now.minute - (time_now.minute % 5)
time_rounded = time_now.replace(minute=prev_minute, second=0, microsecond=0)

while True:
    # Wait until next 5 minute time
    time_rounded += timedelta(minutes=5)
    time_to_wait = (time_rounded - datetime.datetime.now()).total_seconds()
    time.sleep(time_to_wait)

    # Now run TFL API call

    reply = requests.get("https://api.tfl.gov.uk/Line/Elizabeth/Status")

    data = reply.json()

    Status = (data[0]["lineStatuses"][0]["statusSeverityDescription"])

# fixed to look at only journeys between paddington rail station and ealing broadway
    arrivals = requests.get("https://api.tfl.gov.uk/Journey/JourneyResults/910GPADTON/to/910GEALINGB/")
    data_arrivals = arrivals.json()

    destination = data_arrivals["journeys"][0]["legs"][0]["instruction"]["detailed"]
    second_train = data_arrivals["journeys"][1]["legs"][0]["instruction"]["detailed"]
    departtime = data_arrivals["journeys"][0]["legs"][0]["departureTime"]
    secondtime = data_arrivals["journeys"][1]["legs"][0]["departureTime"]
    #platform = data_arrivals["journeys"][0]["legs"][0]["instruction"]["platform"]

    now = datetime.datetime.now()
    now = (now.strftime("%Y-%m-%d %H:%M"))
    msg = "Update: " + now + "\n" + "Elizabeth Line: " + Status + "\n\n" + "Next train: " + destination + ", " + departtime + "\n" + "Second train: " + second_train + ", " + secondtime
    print(msg)

    # Send a WhatsApp Message to a Contact at 1:30 PM
    pywhatkit.sendwhatmsg_instantly("+447845662324", msg, 10, True, 3)

