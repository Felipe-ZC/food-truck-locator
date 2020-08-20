# food-truck-locator
A command-line utility that returns the names and addresses of all the currently open food trucks in San Francisco.

# Supported Platforms
Any Linux distro with kernel version 5.4

# Setup
Make sure you have ```python 3.4+``` and ```pip3``` installed!
Please refer to their respective docs for installation support.

Once you have python3 and pip3 working correctly on your system,
run the following commands to install dependencies:
```
git clone https://github.com/Felipe-ZC/food-truck-locator.git
cd food-truck-locator/
pip3 install -r requirements.txt # install dependencies 
```

After installing dependencies, please create a config file in ```utils/``` 
that contains the URL of the Mobile Food Schedule dataset:
```
{
	"host" : dataSetUrl
}
```

The config file is not necessary, however, if no config file
is used, the user MUST specify the host url when creating a 
new ```FoodTruckSchedule``` object:

```
ftFinder = FoodTruckFinder(dataSetUrl)
```
