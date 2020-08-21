#!/usr/bin/env python3
import sys
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
    
    def getTimeData(self):
        # Python and Socrata both use ints in the range [0,6] to represent days of the week 
        # but Python's week starts on Monday while Socrata starts on Sunday.
        weekday = (datetime.today().weekday() + 1) % 7 # Compute Socrata day of week
        currHour = str(datetime.now().strftime("%H:%M")) # Current hour in 24-hour format
        return weekday, currHour 
    
    def getTrucksOpenNow(self, limit, offset, tz=""):
        # Get current time
        try: timeObj = datetime.now() if not tz else datetime.now(timezone(tz))
        except Exception as e: raise RuntimeError(f"Invalid timezone: {e}") 
        weekday, currHour = self.getTimeData()        
        return self.fts.getTrucksOpenAt(limit, offset, weekday, currHour)
    
    def run(self, limit=10, offset=10):
        userIn = ""
        currPage = 0
        while userIn != 'q':
            userIn = input(f"Press 'n' to load the next {limit} food trucks or 'q' to quit: ")
            if userIn == 'n':                
                print("Fetching food trucks...\n")
                try:
                    nextRows = self.getTrucksOpenNow(limit, currPage)
                    if not nextRows or len(nextRows) < limit:
                        print("There are no more food trucks open right now.")
                        break
                    print(self.formatOutput(nextRows) + "\n")
                    currPage += offset 
                except Exception as e: 
                    print(f"Error! Exception encountered while processing food truck data:\n{e}")
                    break
                    
if __name__ == "__main__":
    print("Welcome to Food Truck Finder!")
    ftFinder = FoodTruckFinder()
    ftFinder.run()
