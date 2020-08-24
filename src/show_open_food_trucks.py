import sys
from requests.exceptions import HTTPError, ConnectionError
from .food_truck_utils.food_truck_finder import FoodTruckFinder


class ShowOpenFoodTrucks:
    def __init__(self):
        self.food_finder = FoodTruckFinder()

    def run(self, limit=10, offset=10, time_zone=""):
        """
        Retrieves and displays open food trucks in San Francisco,
        at the current local time.

        Program fetches and displays 'limit' items, waits for user
        input to fetch and display the next 'limit' items.

        Parameters:
            limit (int): Max. number of rows to return
            offset (int): Offset count into the results
            time_zone (string): A string representation of the TZ database
                                to use when calculating local time.
        Returns:
            None
        """
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
        # Hide KeyboardInterrupt stacktrace
        except KeyboardInterrupt:
            print("\nInterrupted")
            sys.exit(0)
        # Hide stacktrace on EOF(^D on linux, ^Z on windows)
        except EOFError:
            print("\nError! EOF reached while reading input.")
            sys.exit(1)
        except (ValueError, RuntimeError, HTTPError, ConnectionError) as err:
            print(
                f"Error! Exception encountered while processing food truck data:\n{err}"
            )
            sys.exit(1)

    @staticmethod
    def format_output(trucks):
        output = [
            f"\"{truck['applicant']}\" \"{truck['location']}\""
            for truck in trucks
        ]
        return "Name Address\n" + "\n".join(output)

    @staticmethod
    def should_get_next_rows(limit):
        """Prompts user for input until they enter 'n' or 'q'.
        Returns True if the last value entered was 'n'."""
        user_in = ""
        while user_in not in ("n", "q"):
            user_in = input(
                f"Press 'n' to load the next {limit} food trucks or 'q' to quit: "
            )
        return user_in == "n"
