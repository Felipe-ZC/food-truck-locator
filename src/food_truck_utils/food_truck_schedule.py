import requests
from requests.utils import requote_uri


class FoodTruckSchedule:
    def __init__(self, host_url=""):
        # The URL of Mobile Food Schedule dataset...
        self.url = host_url

    def get_trucks_open_at(self, limit, offset, day, time):
        """
        Returns all food truck names and addresses that are currently open
        at the given day and hour. Results are sorted by food truck name.
        Raises HTTPError on failed queries, raises ValueError when response
        body contains invalid JSON.
        
        Parameters:
            limit (int): Max. number of rows to return
            offset (int): Offset count into the results
            day (int): An integer ranging from [0,6] representing the day of
                       the week (Sunday = 0, Monday = 1, etc.)
            time (string): A string representation of the current time,
                           that is, the current hour and minutes ("%H:%M")

        Returns:
            A JSON object containing the name and addresses of
            each food truck open at the given time.
        
        Raises:
            HTTPError: On response status codes >= 400.
            ValueError: When response body contains invalid JSON.
        """
        # Implicit concatenation...
        query = (
            f"$select=applicant, location &"
            f"$where=dayorder={day} and '{time}' >= start24 and '{time}' < end24 &"
            f"$limit={limit} &"
            f"$offset={offset} &"
            f"$order=applicant")
        return self.process_query(query)

    def process_query(self, query):
        """
        Returns the result of a SoQL query as a list of dicts. Each dict
        contains the attributes specified in the select clause of the given
        query. Raises HTTPError on failed queries, raises ValueError when 
        response body contains invalid JSON.

        Parameters:
            query (string): SoQL query

        Returns:
            A JSON object containing the results of the given query

        Raises:
            HTTPError: On response status codes >= 400.
            ValueError: When response body contains invalid JSON.
        """
        req_url = self.url + "?" + query
        # Always encode request uri as specified in Socrata's API docs
        response = requests.get(requote_uri(req_url),
                                headers={"content-type": "application/json"})
        
        if response.status_code >= 400:
            response.raise_for_status() 
        
        try:
            data = response.json()
        except ValueError as err:
            raise ValueError(f"Response contains invalid JSON: {err}")

        return data
