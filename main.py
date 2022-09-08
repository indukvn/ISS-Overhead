import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 20.593683
MY_LNG = 78.962883

email = "your@gmail.com"
password = "your_password"


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    if MY_LAT-5 <= latitude <= MY_LAT+5 and MY_LNG-5 <= longitude <= MY_LNG+5:
        return True


def is_night():
    params = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=params)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(email, password)
        connection.sendmail(
            from_addr=email,
            to_addrs=email,
            msg="Subject: Look Up\n\nThe ISS is above in the sky."
        )
