# food-truck-locator
A command-line utility that returns the names and addresses of all the currently open food trucks in San Francisco.

### Supported Platforms

- Any Linux distro with kernel version 5.4
- Windows 10

### Setup
Make sure you have ```python 3.7```  or higher and ```pip3``` installed!
Please refer to their respective docs for installation support.
You can check what version of python you are using by running:
```
python --version 
# On some systems python3+ is installed separately... 
python3 --version 
```

**This script will not work with any python version less than 3.7!**

Once you have python3 and pip3 working correctly on your system,
run the following commands to clone this repo and install dependencies:

```
git clone https://github.com/Felipe-ZC/food-truck-locator.git
cd food-truck-locator/
pip3 install -r requirements.txt # install dependencies 
```

### Running
To execute the food-truck-locator script, run the following command
in your terminal:
```
python main.py
# On some systems python3+ is installed separately... 
python3 main.py 
```

We can make the showOpenFoodTrucks python script executable on Unix
like systems using the following command:
```
chmod +x main.py
./main.py 
```
