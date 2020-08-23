from .food_truck_utils.food_truck_finder import FoodTruckFinder


class ShowOpenFoodTrucks:
    def __init__(self):
        self.food_finder = FoodTruckFinder()

    def run(self, limit=10, offset=10, time_zone=""):
        print("Welcome to Food Truck Finder!")
        try:
            # For all the open food trucks...
            for trucks in self.food_finder.get_next_open_trucks(
                    limit, offset, time_zone):
                print(self.format_output(trucks) + "\n")
                if len(trucks) < limit:
                    break
                if not self.should_get_next_rows(limit):
                    return
            print("There are no more open food trucks right now.")
        except Exception as err:
            print(
                f"Error! Exception encountered while processing food truck data:\n{err}"
            )

    @staticmethod
    def should_get_next_rows(limit):
        user_in = ""
        while user_in not in ('n', 'q'):
            user_in = input(
                f"Press 'n' to load the next {limit} food trucks or 'q' to quit: "
            )
        return user_in == "n"

    @staticmethod
    def format_output(trucks):
        output = [
            f"\"{truck['applicant']}\" \"{truck['location']}\""
            for truck in trucks
        ]
        return "Name Address\n" + "\n".join(output)
