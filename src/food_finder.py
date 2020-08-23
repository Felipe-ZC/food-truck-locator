from .utils.mobile_food_util import FoodTruckSchedule
from datetime import datetime
from pytz import timezone

'''
Pass in time object from 
'''

class FoodTruckFinder:
    def __init__(self):
        # To make testing easier I've hardcoded the URL, although
        # using a config file is the right way to go!
        self.fts = FoodTruckSchedule("https://data.sfgov.org/resource/jjew-r69b.json")
 
    def get_trucks_open_now(self, limit, offset, tz="", quiet=False):
        time_obj = self.get_time_obj(tz)
        # Python and Socrata both use ints in the range [0,6] to represent days of the week
        # but Python's week starts on Monday while Socrata starts on Sunday.
        weekday = (time_obj.weekday() + 1) % 7
        # Current hour and minutes in 24-hour format
        curr_time = time_obj.strftime("%H:%M")
        print(self.get_loading_msg(time_obj))
        return self.fts.get_trucks_open_at(limit, offset, weekday, curr_time)
    
    def get_next_open_trucks(self, limit, offset, tz=""):
        page_start = 0
        trucks = self.get_trucks_open_now(limit, page_start)
        while trucks:
            yield trucks
            page_start += offset
            trucks = self.get_trucks_open_now(limit, page_start, tz)

    def get_time_obj(self, tz=""):
        try:
            time_obj = datetime.now() if not tz else datetime.now(timezone(tz))
        except Exception as e:
            raise RuntimeError(f"Invalid timezone: {e}")
        return time_obj

    def get_loading_msg(self, time_obj=None):
        if not time_obj:
            time_obj = self.get_time_obj()
        return (
            f"Looking for food trucks open on {time_obj.strftime('%A, %m/%d/%Y at %I:%M %p')}...\n"
        )

    def format_output(self, trucks):
        output = [
            f"\"{truck['applicant']}\" \"{truck['location']}\"" for truck in trucks
        ]
        return "Name Address\n" + "\n".join(output)


