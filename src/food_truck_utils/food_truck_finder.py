from datetime import datetime
from pytz import timezone
from .food_truck_schedule import FoodTruckSchedule

# limit, offset and timezone as instance vars?


class FoodTruckFinder:
    def __init__(self):
        # To make testing easier I've hardcoded the URL, although
        # using a config file is the right way to go!
        self.fts = FoodTruckSchedule(
            "https://data.sfgov.org/resource/jjew-r69b.json")

    def get_trucks_open_now(self, limit, offset, _tz="", quiet=False):
        time_obj = self.__get_time_obj(_tz)

        # Python and Socrata both use ints in the range [0,6] to represent days of the week
        # but Python's week starts on Monday while Socrata starts on Sunday.
        weekday = (time_obj.weekday() + 1) % 7
        # Current hour and minutes in 24-hour format
        curr_time = time_obj.strftime("%H:%M")

        if not quiet:
            print(self.__get_loading_msg(time_obj))

        return self.fts.get_trucks_open_at(limit, offset, weekday, curr_time)

    def get_next_open_trucks(self, limit, offset, _tz=""):
        page_start = 0
        trucks = self.get_trucks_open_now(limit, page_start)

        while trucks:
            yield trucks
            page_start += offset
            trucks = self.get_trucks_open_now(limit, page_start, _tz)

    @staticmethod
    def __get_time_obj(_tz=""):
        try:
            time_obj = datetime.now() if not _tz else datetime.now(
                timezone(_tz))
        except Exception as err:
            raise RuntimeError(f"Invalid timezone: {err}")
        return time_obj

    @staticmethod
    def __get_loading_msg(time_obj):
        return (
            f"Looking for food trucks open on {time_obj.strftime('%A, %m/%d/%Y at %I:%M %p')}...\n"
        )
