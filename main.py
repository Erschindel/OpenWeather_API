import requests
import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

API_KEY = os.environ["OPENWEATHERMAP_KEY"]
LAT = os.environ["MY_LAT"]
LON = os.environ["MY_LON"]

request_URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&APPID={API_KEY}"

try:
    r = requests.get(request_URL)
    data = r.json()
    print("Success")
except:
    print("failed to connect")

minutelyData = data["minutely"]
currentTimestamp = data["minutely"][0]["dt"]
currentTime = dt.datetime.fromtimestamp(int(currentTimestamp)).strftime('%H:%M')

def updateData () :
    writeCount = 0
    with open("data/minutely.csv", "w") as new_file :
        file_writer = csv.writer(new_file)
        for datum in minutelyData :
            file_writer.writerow([minutelyData[writeCount]["dt"], minutelyData[writeCount]["precipitation"]])
            writeCount += 1
        return "csv file updated"

def graphForecast () :
    x, y = np.loadtxt("data/minutely.csv", delimiter = ",", unpack = True)

    dateconv = np.vectorize(dt.datetime.fromtimestamp)
    xTime = dateconv(x)
    print(type(xTime))

    plt.plot(xTime, y)
    plt.xlabel("time (min)")
    plt.ylabel("precipitation (mm)")
    plt.title("Predicted rainfall")
    plt.ylim(-1, 30)
    plt.show()
    return "Success"

currentRainVolume = data["minutely"][0]["precipitation"]
hourlyRainChange = currentRainVolume - data["minutely"][60]["precipitation"]

def rainNextHour() :
    ans = f"{currentRainVolume}mm (+{abs(hourlyRainChange)}mm predicted in the next hour)"
    if hourlyRainChange < 0 :
        ans = ans.replace("+", "-")
    return ans

print(currentTime)
