import requests
import json
from requests.utils import requote_uri

class FoodTruckSchedule:
    def __init__(self, apiHost=""):
        self.url = apiHost

    def getTrucksOpenAt(self, limit, offset, day, time):
        '''
        Returns all food truck names and addresses that are currently open 
        at the given day and hour. Results are sorted by food truck name.

            Paramters:
                limit (int): Max. number of rows to return
                offset (int): Offset count into the results
                day (int): An integer ranging from [0,6] representing the day of the week (Sunday = 0, Monday = 1, etc.)
                time (string): A string representation of the current time, that is, the current hour and minutes ("%H:%M")

            Returns:
                data (list): A list of dicts that contains the name and address of each food truck open at the given time.
        '''
        # Implicit concatenation...
        query = (f"$select=applicant, location &"
                 f"$where=dayorder={day} and '{time}' >= start24 and '{time}' < end24 &"
                 f"$limit={limit} &"
                 f"$offset={offset} &"
                 f"$order=applicant")
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
        # Always encode request uri as specified in Socrata's API docs
        response = requests.get(requote_uri(reqUrl)) 
        if response.status_code == 200: data = response.json()
        else: response.raise_for_status()
        return data
