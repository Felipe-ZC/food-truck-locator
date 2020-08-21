import requests
import json
import os
from datetime import datetime
from pytz import timezone
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
    
    def getOpenTrucksNowPdt(self, limit, offset):
        '''
        Returns all food truck names and addresses that are currently open 
        at the current day and hour in San Francisco. This function uses time 
        in PDT, if you wish to specify a different time please use getOpenTrucksAt.

            Paramters:
                limit (int): Max. number of rows to return
                offset (int): Offset count into the results

            Returns:
                data (list): A list of dicts that contains the name and address of each food truck open currently.
        '''
        # Get current time in California
        pdt = datetime.now(timezone("America/Los_Angeles"))
        # Python and Socrata both use ints in the range [0,6] to represent days of the week 
        # but Python's week starts on Monday while Socrata starts on Sunday.
        weekday = (pdt.today().weekday() + 1) % 7 # Compute Socrata day of week
        currHour = str(pdt.strftime("%H:00")) # Current hour in 24-hour format
        return self.getOpenTrucksAt(limit, offset, weekday, currHour)

    def getOpenTrucksNow(self, limit, offset):
        '''
        Returns all food truck names and addresses that are currently open 
        at the current day and hour using system time. 

            Paramters:
                limit (int): Max. number of rows to return
                offset (int): Offset count into the results

            Returns:
                data (list): A list of dicts that contains the name and address of each food truck open currently.
        '''
        # Python and Socrata both use ints in the range [0,6] to represent days of the week 
        # but Python's week starts on Monday while Socrata starts on Sunday.
        weekday = (datetime.today().weekday() + 1) % 7 # Compute Socrata day of week
        currHour = str(datetime.now().strftime("%H:00")) # Current hour in 24-hour format
        return self.getOpenTrucksAt(limit, offset, weekday, currHour)
    
    def getOpenTrucksAt(self, limit, offset, day, hour):
        '''
        Returns all food truck names and addresses that are currently open 
        at the given day and hour. Results are sorted by food truck name.

            Paramters:
                limit (int): Max. number of rows to return
                offset (int): Offset count into the results
                day (int): An integer ranging from [0,6] representing the day of the week (Sunday = 0, Monday = 1, etc.)
                hour: (string): A string representation of the current time in 24 hour format ("%H:00")

            Returns:
                data (list): A list of dicts that contains the name and address of each food truck open at the given time.
        '''
        query = f"$select=applicant,location&$where=dayorder={day} and '{hour}' >= start24 and '{hour}' < end24&$limit={limit}&$offset={offset}&$order=applicant"
        return self.processQuery(query)
    
    def processQuery(self, query):
        '''
        Returns the result of a SoQL query as a list of dicts. Each dict contains
        the attributes specified in the select clause of the given query. 

            Paramters:
                query(string): SoQL query

            Returns:
                data (list): A list of dicts containing the results of the given query.
        '''
        reqUrl = self.url + "?" + query 
        data = None
        response = requests.get(requote_uri(reqUrl)) # Always encode request uri as specified in Socrata's API docs
        if response.status_code == 200: data = response.json()
        else: response.raise_for_status()
        return data
