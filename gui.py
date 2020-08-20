import npyscreen
from mobile_food_util import FoodTruckSchedule 

class FoodTruckFinder(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.registerForm("MAIN", MainForm())

class TextArea(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit

# This form class defines the display that will be presented to the user.
class MainForm(npyscreen.Form):
    def create(self):
        # Initialize API util...
        self.ftUtil = FoodTruckSchedule()
        self.offset = 0
        # Set title
        self.name = "Food Truck Finder 3000"
        # Add user prompt and data output field to the form
        # Make both boxes one fifth of the total useable area...
        x,y = self.useable_space()
        self.prompt = "Please press Enter to load next 10 rows or Ctrl+C to exit"
        self.UserPrompt = self.add(TextArea, max_height=y//10, value=self.prompt, editable=False)
        self.TruckData = self.add(TextArea, max_height=y//5, editable=False)
        # Add any necessary handlers
        handlers = { "^A": self.myFunc, }
        self.add_handlers(handlers)

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def myFunc(self, event):
        self.TruckData.value = "Fetching data..."
        self.TruckData.display()
        try:
            data = self.ftUtil.get_next_rows(10, self.offset) 
            self.TruckData.value = str(data)
            self.offset += 10
        except:
            self.TruckData.value = "Error while fetching data!"
        self.TruckData.display()


if __name__ == '__main__':
    ft_finder = FoodTruckFinder()
    ft_finder.run()
