#!/usr/bin/env python3
from food_truck_utils.food_truck_finder import FoodTruckFinder

class ShowOpenFoodTrucks: 
    def __init__(self):
        # To make testing easier I've hardcoded the URL, although
        # using a config file is the right way to go!
        self.food_finder = FoodTruckFinder()

    def run(self, limit=10, offset=10, tz=""):
        print("Welcome to Food Truck Finder!")
        try:
            # For all the open food trucks...
            for trucks in self.food_finder.get_next_open_trucks(limit, offset, tz):
                print(self.food_finder.format_output(trucks) + "\n")
                if len(trucks) < limit:
                    break

                user_in = ""
                while user_in != "n":
                    user_in = input(
                        f"Press 'n' to load the next {limit} food trucks or 'q' to quit: "
                    )
                    if user_in == "q":
                        return
            
            print("There are no more open food trucks right now.")
        except Exception as e:
            print(
                f"Error! Exception encountered while processing food truck data:\n{e}"
            )

if __name__ == "__main__":
    app = ShowOpenFoodTrucks()
    app.run()
    print("Goodbye.")
