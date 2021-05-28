import json
import time
import requests
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import urllib
import configparser
from py_linq import Enumerable
from datetime import datetime

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
}


def readCowinAPI(district_id):
    todayDate = datetime.today().strftime('%d-%m-%Y')
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={0}&date={1}".format(
        district_id, todayDate)
   
    result = GetWebRequestData(url)
    centers = result["centers"]

    for key in centers:
        for sessionkey in key["sessions"]:
            message = ""
            if(sessionkey["min_age_limit"] == 18 and sessionkey["available_capacity"] > 0):
                message += ("%s Pincode - %s\n" %
                            (sessionkey["date"], key["pincode"]))
                message += ("%s" % (key["name"]))
                message += ("\n%s Stock - %s - %s" %
                            (key["fee_type"], sessionkey["vaccine"], sessionkey["available_capacity"]))

                # print(message)
                sendToTelegram(message)
                break


def GetWebRequestData(url):
    data = requests.get(url, headers=headers)
    data = data.json()
    return data


def sendToTelegram(text):
    urlString = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}"

    config = configparser.ConfigParser()
    config.read(r'D:\Hobby Projects\VaccinationAlerts\CONFIGURATON.INI')

    # Give api token of the bot
    apiToken = config.get('TELEGRAM', 'API_TOKEN')
    chatId = config.get('TELEGRAM', 'CHAT_ID')

    text = text.replace("&", "And")
    for i in range(0, len(text), 3800):
        url = urlString.format(
            apiToken,chatId, text[i:i+3800])
        response = requests.get(url)



def readCowinAPIByPincode(pincode):
    todayDate = datetime.today().strftime('%d-%m-%Y')
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={0}&date={1}".format(
        pincode, todayDate)
    print(url)
    result = GetWebRequestData(url
                               )

    centers = result["centers"]

    for key in centers:
        for sessionkey in key["sessions"]:
            message = ""
            if(sessionkey["min_age_limit"] == 18 and sessionkey["available_capacity"] > 0):
                message += ("%s Pincode - %s\n" %
                            (sessionkey["date"], key["pincode"]))
                message += ("%s" % (key["name"]))
                message += ("\n%s Stock - %s - %s" %
                            (key["fee_type"], sessionkey["vaccine"], sessionkey["available_capacity"]))

                # print(message)
                sendToTelegram(message)
                break

readCowinAPI(278) #Hubli
# readCowinAPI(293)
# readCowinAPI(294)
readCowinAPIByPincode(580031) 