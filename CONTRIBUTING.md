# Read This First!

Hello! I'm glad you're considering to contribute to Genshin Stopwatch!

**Mobile contribution is a WIP at the moment, so please ignore any information reguarding it**

Before reading, please keep in mind there are two versions of Genshin Stopwatch:
+ A desktop version written in Python with PyQt5
+ A mobile version written in C# with .NET Maui

Both versions are located within `/src` in their own seperate folders

# How to debug desktop:

## Rules and Tips:
+ If running with the script, remember to change directory to `main.py`'s directory before running in your IDE.
+ Remember to ALWAYS discard changes to `save.txt` and `config.ini` before pushing commits
+ When creating a new config setting, always make a fallback value.
+ `guide.html` runs on a limited version of HTML 4
+ In `main.py`, all code after defining classes are treated like global values, this is where you will find file paths and initialization.
+ `styles.py` is the program's style manager, anything involving styles goes in there.

## Creating the executable

Genshin stopwatch already knows if you're running from the script or an executable and auto-adjusts file paths.
But things may work differently depending if it's from the script or not.

To manually create the executable, change your directory to the script and then copy and paste this command into your preferred command line.
```bash
pyinstaller --clean main.spec --distpath ./
```

After pyinstaller is finished what it does best, there should be a build folder and the exe in the root folder.
From there you can run the executable like normal.

If you want a console to run to make debugging in the executable easier, edit the `main.spec` and change this line.
```py
console=True
```
**Remember to discard changes or change this value back to False when pushing commits**

## Notifications

### Forcing a notification
To force a notification, just include this line after `NotificaionPanel`'s initalization:
```py
notify.Notify("Finished Timer name goes here")
```
