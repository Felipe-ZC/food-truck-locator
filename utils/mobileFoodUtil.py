import requests
import json
import os
from datetime import datetime
from requests.utils import requote_uri

class FoodTruckSchedule:
    def __init__(self, apiHost=""):
        self.url = apiHost
        # If the host has not been provided, look in config file
        if not self.url:
            try:
                config = self.__getConfig()
                self.url = config["host"]         
            except Exception as e: 
                raise RuntimeError(f"Missing or invalid config file: {e}")

    def __getConfig(self):
        scriptPath = os.path.dirname(os.path.realpath(__file__))
        filePath = os.path.join(scriptPath, "config.json")
        with open(filePath) as config:
            return json.load(config)
    
    '''
    Select all truck names and addresses that are currently open.
    'Currently open' means that the truck is operating on the current
    day of the week and the current time is between the start and end
    times of the food truck.
    '''
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

    def processQuery(self, query):
        reqUrl = self.url + "?" + query 
        data = None
        response = requests.get(requote_uri(reqUrl)) # Always encode request uri as specified in Socrata's API docs
        if response.status_code == 200: data = response.json()
        else: response.raise_for_status()
        return data

