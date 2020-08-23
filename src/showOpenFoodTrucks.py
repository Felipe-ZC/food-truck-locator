#!/usr/bin/env python
from utils.mobileFoodUtil import FoodTruckSchedule
from datetime import datetime
from pytz import timezone


class FoodTruckFinder:
    def __init__(self):
        # To make testing easier I've hardcoded the URL, although
        # using a config file is the right way to go!
        self.fts = FoodTruckSchedule("https://data.sfgov.org/resource/jjew-r69b.json")

    def run(self, limit=10, offset=10):
        print("Welcome to Food Truck Finder!")
        try:
            print(self.getLoadingMsg())
            # For all the open food trucks...
            for trucks in self.getNextOpenTrucks(limit, offset):
                print(self.formatOutput(trucks) + "\n")
                if len(trucks) < limit:
                    break

                userIn = ""
                while userIn != "n":
                    userIn = input(
                        f"Press 'n' to load the next {limit} food trucks or 'q' to quit: "
                    )
                    if userIn == "q":
                        return

                print(self.getLoadingMsg())

            print("There are no more open food trucks right now.")
        except Exception as e:
            print(
                f"Error! Exception encountered while processing food truck data:\n{e}"
            )

    def getTrucksOpenNow(self, limit, offset, tz=""):
        timeObj = self.getTimeObj(tz)
        # Python and Socrata both use ints in the range [0,6] to represent days of the week
        # but Python's week starts on Monday while Socrata starts on Sunday.
        weekday = (timeObj.weekday() + 1) % 7
        # Current hour and minutes in 24-hour format
        currTime = timeObj.strftime("%H:%M")
        return self.fts.getTrucksOpenAt(limit, offset, weekday, currTime)

    def getNextOpenTrucks(self, limit, offset):
        currPage = 0
        nextRows = self.getTrucksOpenNow(limit, currPage)
        while nextRows:
            yield nextRows
            currPage += offset
            nextRows = self.getTrucksOpenNow(limit, currPage)

    def getTimeObj(self, tz=""):
        try:
            timeObj = datetime.now() if not tz else datetime.now(timezone(tz))
        except Exception as e:
            raise RuntimeError(f"Invalid timezone: {e}")
        return timeObj

    def getLoadingMsg(self, timeObj=None):
        if not timeObj:
            timeObj = self.getTimeObj()
        return (
            f"Looking for food trucks open on {timeObj.strftime('%A at %I:%M %p')}...\n"
        )

    def formatOutput(self, trucks):
        outputStr = [
            f"\"{truck['applicant']}\" \"{truck['location']}\"" for truck in trucks
        ]
        return "Name Address\n" + "\n".join(outputStr)


if __name__ == "__main__":
    ftFinder = FoodTruckFinder()
    ftFinder.run()
    print("Goodbye.")
