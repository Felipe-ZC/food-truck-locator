#!/usr/bin/env python
from utils.mobileFoodUtil import FoodTruckSchedule
from datetime import datetime
from pytz import timezone

class FoodTruckFinder:
    def __init__(self):
        # To make testing easier I've hardcoded the URL, although 
        # using a config file is the right way to go!
        self.fts = FoodTruckSchedule("https://data.sfgov.org/resource/jjew-r69b.json")

    def formatOutput(self, trucks):
        outputStr = [f"\"{truck['applicant']}\" \"{truck['location']}\"" for truck in trucks]
        return "Name Address\n" + "\n".join(outputStr)
     
    def getTrucksOpenNow(self, limit, offset, tz=""):
        # Python and Socrata both use ints in the range [0,6] to represent days of the week 
        # but Python's week starts on Monday while Socrata starts on Sunday.
        try: timeObj = datetime.now() if not tz else datetime.now(timezone(tz)) # Get current time
        except Exception as e: raise RuntimeError(f"Invalid timezone: {e}") 
        weekday = (timeObj.weekday() + 1) % 7 # Compute Socrata day of week
        currHour = str(timeObj.strftime("%H:%M")) # Current hour in 24-hour format
        return self.fts.getTrucksOpenAt(limit, offset, weekday, currHour)
    
    def getNextOpenTrucks(self, limit, offset):
        currPage = 0
        nextRows = self.getTrucksOpenNow(limit, currPage)
        while nextRows:
            yield nextRows
            currPage += offset
            nextRows = self.getTrucksOpenNow(limit, currPage)

    def run(self, limit=10, offset=10):
        print("Welcome to Food Truck Finder!\nFetching data...\n")
        try:
            # For all the open food trucks...
            for trucks in self.getNextOpenTrucks(limit, offset):    
                userIn = ""
                print(self.formatOutput(trucks) + "\n")
                if len(trucks) < limit: break
                while userIn != 'n': 
                    if userIn == 'q': return 
                    userIn = input(f"Press 'n' to load the next {limit} food trucks or 'q' to quit: ")
                print("Fetching data...\n")
            # Done
            print("There are no more open food trucks right now.")
        except Exception as e:
            print(f"Error! Exception encountered while processing food truck data:\n{e}")
 
if __name__ == "__main__":
    ftFinder = FoodTruckFinder()
    ftFinder.run()
    print("Goodbye.")
