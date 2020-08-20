#!/usr/bin/env python
import requests
import json
import os
from datetime import datetime
from requests.utils import requote_uri
'''
1) Get current day of the week and hour
2) Query using SoQL to get food trucks that are open
   on the current day of the week:
   $select=*
   $where=dayorder={day_of_week}
'''
class FoodTruckSchedule:
    def __init__(self, apiHost="", configDir=""):
        self.url = apiHost
        # If the host has not been provided, look in config file
        if not self.url:
            config = self.__getConfig(configDir)
            self.url = config["host"]         

    def __getConfig(self, configDir=""):
        scriptPath = os.path.dirname(os.path.realpath(__file__))
        filePath = os.path.join(scriptPath, configDir or "config.json")
        with open(filePath) as config:
            return json.load(config)

    def getOpenTrucksNow(self, limit, offset):
        weekday = (datetime.today().weekday() + 1) % 7
        currHour = str(datetime.now().strftime("%H:00"))
        query = f"$select=applicant, location&$where=dayorder={weekday} and '{currHour}' >= start24 and end24 < '{currHour}'&$limit={limit}&$offset={offset}&$order=applicant"
        return self.getNextRows(limit, offset, query)

    def getNextRows(self, limit, offset, query=""):
        reqUrl = self.url + "?" + query 
        data = None
        response = requests.get(requote_uri(reqUrl))

        if response.status_code == 200: data = response.json()
        else: raise RuntimeError(response.json()) 
        
        return data

