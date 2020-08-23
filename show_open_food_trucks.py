#!/usr/bin/env python3
from food_truck_utils.food_truck_finder import FoodTruckFinder

class ShowOpenFoodTrucks: 
    def __init__(self):
        self.food_finder = FoodTruckFinder()

    def run(self, limit=10, offset=10, tz=""):
        print("Welcome to Food Truck Finder!")
        try:
            # For all the open food trucks...
            for trucks in self.food_finder.get_next_open_trucks(limit, offset, tz):
                print(self.format_output(trucks) + "\n")     
                if len(trucks) < limit:
                    break
                if not self.shouldGetNextRows(limit):
                    return
            print("There are no more open food trucks right now.")
        except Exception as e:
            print(
                f"Error! Exception encountered while processing food truck data:\n{e}"
            )

    def shouldGetNextRows(self, limit):
        user_in = ""
        while user_in != "n" and user_in != "q":
            user_in = input(
                f"Press 'n' to load the next {limit} food trucks or 'q' to quit: "
            )
        return user_in == "n"

    def format_output(self, trucks):
        output = [
            f"\"{truck['applicant']}\" \"{truck['location']}\"" for truck in trucks
        ]
        return "Name Address\n" + "\n".join(output)


if __name__ == "__main__":
    app = ShowOpenFoodTrucks()
    app.run()
    print("Goodbye.")
