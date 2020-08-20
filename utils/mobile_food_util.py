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
        filePath = os.path.join(scriptPath, "config.json")
        with open(configDir or filePath) as config:
            return json.load(config)

    
    # Select all truck names and addresses that are currently open  
    def getOpenTrucksNow(self, limit, offset):
        '''
        weekday is an integer representation of the day of the week (Monday,Tuesday, etc.)
        Python and Socrata both use ints in the range [0,6] to represent but Python starts
        counting position 0 at Monday while Socrata starts at Sunday.
        '''
        weekday = (datetime.today().weekday() + 1) % 7 # Compute Socrata day of week
        currHour = str(datetime.now().strftime("%H:00")) # Current hour in 24-hour format
        query = f"$select=applicant,location&$where=dayorder={weekday} and '{currHour}' >= start24 and '{currHour}' < end24&$limit={limit}&$offset={offset}&$order=applicant"
        return self.processQuery(query)

    def getAllFoodTrucks(self, limit, offset):
        query = f"$select=applicant,location&$limit={limit}&$offset={offset}&$order=applicant"
        return self.processQuery(query)
    
    def processQuery(self, query=""):
        reqUrl = self.url + "?" + query 
        data = None
        # Always encode request uri as specified in Socrata's API docs
        response = requests.get(requote_uri(reqUrl))

        if response.status_code == 200: data = response.json()
        else: raise RuntimeError(response.json()) 
        
        return data

