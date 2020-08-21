#!/usr/bin/env python3
from utils.mobileFoodUtil import FoodTruckSchedule
import sys

class FoodTruckFinder:
    def __init__(self):
        # To make testing easier I've hardcoded the URL, although 
        # using a config file is the right way to go!
        try: 
            self.fts = FoodTruckSchedule("https://data.sfgov.org/resource/jjew-r69b.json")
        except Exception as e:
            print(f"Error! Could not instantiate FoodTruckSchedule service.\n{e}")
            sys.exit()

    def formatOutput(self, trucks):
        outputStr = [f"\"{truck['applicant']}\" \"{truck['location']}\"" for truck in trucks]
        return "Name Address\n" + "\n".join(outputStr)

    def run(self, limit=10, offset=10):
        userIn = ""
        currPage = 0
        while userIn != 'q':
            userIn = input(f"Press 'n' to load the next {limit} food trucks or 'q' to quit: ")
            if userIn == 'n':                
                print("Fetching food trucks...\n")
                try:
                    # Use system time by default...
                    nextRows = self.fts.getOpenTrucksNow(limit, currPage)
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
