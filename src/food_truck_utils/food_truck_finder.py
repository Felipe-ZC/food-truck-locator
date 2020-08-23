from datetime import datetime
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError
from .food_truck_schedule import FoodTruckSchedule

class FoodTruckFinder:
    def __init__(self, isQuiet=False):
        # For the sake of the interview I've hardcoded the URL, although
        # using a config file is a better approach!
        self.fts = FoodTruckSchedule(
            "https://data.sfgov.org/resource/jjew-r69b.json")
        self.quiet = isQuiet # Hide/Show loading message

    def get_trucks_open_now(self, limit, offset, _tz=""):
        """
        Retrieves and displays open food trucks in San Francisco
        at the current local time.

        Paramters:
            limit (int): Max. number of rows to return
            offset (int): Offset count into the results
            _tz (string): A string representation of the TZ database
                          to use when calculating local time.
        Returns:
            List of JSON objects, each object contains the name
            and address of the food truck.
        
        Raises:
            HTTPError: On response status codes >= 400.
            ValueError: When response body contains invalid JSON.
            ValueError: Invalid timezone.
        """
        time_obj = self.get_time_obj(_tz)
        # Python and Socrata both use ints in the range [0,6] to
        # represent days of the week but Python's week starts on
        # Monday while Socrata starts on Sunday.
        weekday = (time_obj.weekday() + 1) % 7
        # Current hour and minutes in 24-hour format
        curr_time = time_obj.strftime("%H:%M")

        if not self.quiet:
            print(self.get_loading_msg(time_obj))

        return self.fts.get_trucks_open_at(limit, offset, weekday, curr_time)

    def get_next_open_trucks(self, limit, offset, _tz=""):
        """
        Retrieves all open food trucks in San Francisco using the
        generator pattern. Every time this function is called it
        fetches the next 'limit' items until it recieves an empty
        response. Raises RuntimeError and HTTPError

        Paramters:
            limit (int): Max. number of rows to return
            offset (int): Offset count into the results
            _tz (string): A string representation of the TZ database
                               to use when calculating local time.

        Returns:
            List of JSON objects, each object contains the name
            and address of the food truck.

        Raises:
            HTTPError: On response status codes >= 400.
            ValueError: When response body contains invalid JSON.
            ValueError: Invalid timezone.
        """
        page_start = 0
        trucks = self.get_trucks_open_now(limit, page_start, _tz)

        while trucks:
            yield trucks
            page_start += offset
            trucks = self.get_trucks_open_now(limit, page_start, _tz)

    @staticmethod
    def get_time_obj(_tz=""):
        '''Returns the local time as a datetime object. Takes in an
        optional timezone parameter that is the TZ database name
        Raises ValueError if _tz is invalid'''
        try:
            time_obj = datetime.now() if not _tz else datetime.now(
                timezone(_tz))
        except UnknownTimeZoneError as err:
            raise ValueError(f"Invalid timezone: {err}")
        return time_obj

    @staticmethod
    def get_loading_msg(time_obj):
        '''Takes in a datetime object and returns a string
        representing a loading message containing the current
        date and time.'''
        return (
            f"Looking for food trucks open on "
            f"{time_obj.strftime('%A, %m/%d/%Y at %I:%M %p')}...\n"
        )
