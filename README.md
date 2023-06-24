# Genshin Stopwatch
### A program to help keep track of Genshin Impact's time gates. <img src="icon.png" width="150" height="150">

## What does Genshin Stopwatch do?

Genshin Stopwatch is a program that makes checking timers easier without launching the game (Examples: Stamina, Fishing, Gardening, Enemy Respawns, Parametric Transformer, etc...).

The only caviat is that you have to start the stopwatch yourself!

## How does it work?

Genshin Stopwatch is a program that *does not require an internet connection* to use. When you start up the program it will calculate the difference between when you started the program and when the destination of said timer is.

*You can run the program in the background* or disable it in the settings if you want.

**The program is accessible through the system tray** (Up arrow next to the volume mixer) **when running in the background.**

When a stopwatch finishes, a desktop notification will be played *(Check your windows notification and focus assist settings to make sure they will go off.)*

When you create a stopwatch or close the application, your stopwatches will save to the `save.txt` file. The save file is easily configurable and easy to read.

Here is an example of a stopwatch's save data in `save.txt`:

> [2589221199520] <- This is a unique ID, this is for the computer to read and shouldn't be changed by the user!<br>
> name = Parametric Transformer<br>
> time finished = 2023-05-28 11:34:14<br>
> time original duration = 168:00:00<br>
> border color = #37AA9C<br>
> notes = <br>

## What platforms is this compatible with?

At the moment only Windows machines can run this program, ~~I'm not sure if I plan on making mobile versions.~~
<br>
**There are plans to support Linux and MacOS. (see [#8](https://github.com/Wolfmyths/Genshin-Stopwatch/issues/8))**

**Android and iOS is also underway! Release TBD**

## It doesn't work!

+ Check `save.txt` and make sure it looks in a similar format to the example above.
+ The program needs `save.txt` and `config.ini` to start, so if there isn't one in the directory create a text file with the same name or redownload the program.
+ Genshin Stopwatch only works on `Windows`.
+ Check `config.ini` and make sure it looks similar to when you downloaded the program.
+ If notifications aren't working, go to `action center` and `manage notifications`. `Focus assist settings` can disable notifications when they happen under certain conditions.
+ If you upgraded from a version below 1.4 to 1.4+ but kept your `save.txt` and `settings.txt` the same, then you have outdated save/setting file formats. Please see [save/settings rewrite](https://github.com/Wolfmyths/Genshin-Stopwatch/releases/tag/V1.4) if you want to keep your settings/stopwatches

## Does this program run on system startup?

Yes! But you have to do a couple steps to do so, follow the instructions below.

### How to run program on system startup:
1. Create a shortcut of the .exe
2. Press `win + r`
3. Type in `shell:startup` this will take you to your startup directory
4. Place the shortcut in folder

**You can disable run on startup by going to** `task manager -> startup` 

If you found a bug or crash, please report it to me and show how to replicate the issue if possible.<br>
**Before submitting a bug report please check the known bugs in the release notes before telling me.**

## Future Plans?

+ Touch up on the UI a tiny bit for more clarity
+ MacOS/Linux Support *In development! Release TBD*
+ Slightly better notifications
+ Background pictures to choose from for the timers?
+ Translations? *(Not sure if this is necessary but if people want it I will make an effort)*
+ Mobile version? *In development! Release is still TBD*

If you have a suggestion let me know!

## Contributing

If you want to Contribute you can as long as I have an issue posted its up for grabs! Just make a fork and submit a pull request of your contribution.

If you want to test the exe with PyInstaller, `pip install pyinstaller` and then go to the directory where you cloned the repo and type `pyinstaller --clean main.spec` to package the program

## Credits

Thanks to [PyQt5](https://pypi.org/project/PyQt5/) for making an open source easy-to-use framework.

Thanks to [Win10toast](https://pypi.org/project/win10toast/) and [Apprise](https://pypi.org/project/apprise/) for making it easy to include deskstop notifications.

[Pyinstaller](https://pypi.org/project/pyinstaller/) for creating a way to change python programs into an exe
