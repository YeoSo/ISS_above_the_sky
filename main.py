import requests
from datetime import datetime
import time

# Coordinates for Seoul
SEOUL_LAT = 37.566536
SEOUL_LONG = 126.977966


# Function to check if ISS is close to Seoul above
def is_iss_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(iss_latitude, iss_longitude)

    # Checking if ISS within the range of +- 5
    if SEOUL_LAT - 5 <= iss_latitude <= SEOUL_LAT + 5 and SEOUL_LONG - 5 <= iss_longitude <= SEOUL_LONG + 5:
        return True


# Function to check if it's nighttime
def is_night():
    parameters = {
        "lat": SEOUL_LAT,
        "lng": SEOUL_LONG,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters, )
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Current hour
    time_now = datetime.now().hour

    # Checking if it's night, after Sunset, before Sunrise
    if sunrise >= time_now >= sunset:
        return True


# Updates every 6 seconds and prints when it's within the range
while True:
    if is_iss_close() and is_night():
        print("The ISS station is within your range.")
    time.sleep(6)
