#!/usr/bin/env python
from utils.mobileFoodUtil import FoodTruckSchedule

# Document each class in readme 
class FoodTruckFinder:
    def formatOutput(self, trucks):
        outputStr = [f"\"{truck['applicant']}\" \"{truck['location']}\"" for truck in trucks]
        return "Name Address\n" + "\n".join(outputStr)

    def run(self, limit=10, offset=10):
        fts = FoodTruckSchedule()
        userIn = ""
        currPage = 0
        while userIn != 'q':
            userIn = input(f"Press 'n' to load the next {limit} food trucks or 'q' to quit: ")
            if userIn == 'n':                
                print("Fetching food trucks...\n")
                try:
                    nextRows = fts.getOpenTrucksNow(limit, currPage)
                    if not nextRows or len(nextRows) < limit:
                        print("There are no more food trucks open right now.")
                        break
                    print(self.formatOutput(nextRows) + "\n")
                    currPage += offset 
                except Exception as e:
                    print(f"--- Runtime error ---\n{e}")
                    break

if __name__ == "__main__":
    print("Welcome to Food Truck Finder!")
    ftFinder = FoodTruckFinder()
    ftFinder.run()
