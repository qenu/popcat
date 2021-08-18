# Popcat

This is an autoclicker for popcat.click

Webdrivers should be included in the release, but you can also download it here


[Chrome Webdriver](https://chromedriver.chromium.org/downloads)

## Usage

```py
from popcat import PopCat

cat = PopCat("chromedriver.exe")

cat.start() # starts the thread for clicks

cat.stop() # stops the thread and fetches count

cat.count # shows current count

cat.clickloop() # this is the standalone function
```

Its a simple project using selenium to interact with popcat website

be aware that chromedriver should be placed in the same directory as executable

it was intended that way for simplicity for people that aren't familiar


## Credits

**GO TAIWAN**

all credits should go to selenium and python

I just use their stuff, and I am pretty sure i code like a monkey






