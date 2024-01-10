# Genshin Stopwatch
### A program to help keep track of Genshin Impact's time gates.

<img src="/img/icon.png" width="150" height="150"> ![GitHub all releases](https://img.shields.io/github/downloads/Wolfmyths/Genshin-Stopwatch/total)
                                              ![GitHub contributors](https://img.shields.io/github/contributors/Wolfmyths/Genshin-Stopwatch)
                                              ![Python](https://img.shields.io/badge/Python-3.11-blue)
                                              ![CSharp](https://img.shields.io/badge/CSharp(soon!)-.NET_7-purple)
                                              ![HTML](https://img.shields.io/badge/HTML-4-orange)
                                              
![Desktop Framework](https://img.shields.io/badge/Desktop_Framework-PySide6-green)
![Mobile Framework](https://img.shields.io/badge/Mobile_Framework(soon!)-.NET_Maui-purple)
                                              
![OS](https://img.shields.io/badge/OS-Win|Mac|Linux|Android(TBD)|iOS(TBD)-blue)
                                              
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C4MJZS9)

# FAQ Table of Contents
- [Genshin Stopwatch](#genshin-stopwatch)
    - [A program to help keep track of Genshin Impact's time gates.](#a-program-to-help-keep-track-of-genshin-impacts-time-gates)
- [FAQ Table of Contents](#faq-table-of-contents)
  - [What does Genshin Stopwatch do?](#what-does-genshin-stopwatch-do)
  - [How are my stopwatches saved?](#how-are-my-stopwatches-saved)
  - [What platforms is this compatible with?](#what-platforms-is-this-compatible-with)
  - [It doesn't work!](#it-doesnt-work)
  - [Does this program run on system startup?](#does-this-program-run-on-system-startup)
    - [On Windows:](#on-windows)
    - [On MacOS:](#on-macos)
    - [On Linux:](#on-linux)
  - [Future Plans?](#future-plans)
  - [Contributing](#contributing)
  - [Credits](#credits)

## What does Genshin Stopwatch do?

Genshin Stopwatch is a program that makes checking timers easier without launching the game (Examples: Stamina, Fishing, Gardening, Enemy Respawns, Parametric Transformer, etc...).

<img src="/img/stopwatch_demo.PNG" alt="Windows version of Genshin Stopwatch">

## How are my stopwatches saved?
When you create a stopwatch or close the application, your stopwatches will save to the `save.txt` file. The save file is easily configurable and easy to read.

Here is an example of a stopwatch's save data in `save.txt`:
```
[2589221199520]
name = Respawns
time finished = 2023-05-28 11:34:14
time original duration = 12:00:00
border color = #37AA9C
notes = Hilichurl Camps
```

## What platforms is this compatible with?

Win 10 and up, MacOS, and Linux versions are available.

MacOS/Linux versions are not tested so if there's any issues please submit an issue

**Android and iOS is also underway! Release TBD**

## It doesn't work!

**Please make sure you're on the latest version**

**Before submitting a bug report please check the known bugs in the latest release notes before telling me.**

**On Windows: The program is accessible through the system tray** *(Up arrow next to the volume mixer)* **when running in the background.**

+ Check `save.txt` and make sure it looks in a similar format to the example above.
+ The program needs `save.txt` and `config.ini` to start, so if there isn't one in the directory create a text file with the same name or redownload the program.
+ Genshin Stopwatch only works on `Windows`.
+ Check `config.ini` and make sure it looks similar to when you downloaded the program.
+ If you upgraded from a version below 1.4 to 1.4+ but kept your `save.txt` and `settings.txt` the same, then you have outdated save/setting file formats. Please see [save/settings rewrite](https://github.com/Wolfmyths/Genshin-Stopwatch/releases/tag/V1.4) if you want to keep your settings/stopwatches

If you found a bug or crash, please report it to me and show how to replicate the issue if possible.<br>

## Does this program run on system startup?

Yes! But you have to do a couple steps to do so, follow the instructions below.

### On Windows:
1. Create a shortcut of the .exe
2. Press `win + r`
3. Type in `shell:startup` this will take you to your startup directory
4. Place the shortcut in folder

**You can disable run on startup by going to** `task manager -> startup` 

### On MacOS:
1. Click the Apple icon and click `System Settings`
2. Go to `General -> Login Items`
3. Click the plus button then `Applications -> Select the app -> Open`

**You may need to enable** `Allow in the Background`

### On Linux:
Every distro is different so you have to do this research on your own, sorry. 😓

## Future Plans?

+ Background pictures to choose from for the timers?
+ Translations? *(Not sure if this is necessary but if people want it I will make an effort)*
+ Mobile version? *In development! Release is still TBD*

If you have a suggestion let me know on the issues page or DM me on my socials!

## Contributing

If you want to Contribute you can as long as I have an issue posted its up for grabs!
Just make a fork and submit a pull request of your contribution.

For more information and background knowledge of the program, see [CONTRIBUTING.md](CONTRIBUTING.md)

## Credits

+ [Contributors!](https://github.com/Wolfmyths/Genshin-Stopwatch/graphs/contributors) Without you guys I wouldn't have gotten as far into this project as I would have on my own. <br> You guys have taught me a lot. ❤️

+ [PySide6](https://www.qt.io/qt-for-python) for creating an open source easy-to-use framework.

+ [Pyinstaller](https://pypi.org/project/pyinstaller/) for creating a way to change python programs into an exe.

+ Color Pallets
  - [Timeless](https://lospec.com/palette-list/timeless) AKA Dark by Archer on lospec.com
  - [Light](https://www.color-hex.com/color-palette/106748) by wcburgess on color-hex.com
  - [Pola 5](https://lospec.com/palette-list/pola5) AKA Hydro by |NOXITIVE| on lospec.com
  - [slimy 05](https://lospec.com/palette-list/slimy-05) AKA Dendro by green guy on lospec.com
  - [Spanish Sunset](https://lospec.com/palette-list/spanish-sunset) AKA Pyro by NicoFerra on lospec.com
  - [Sadness](https://lospec.com/palette-list/sadness) AKA Cryo by finn on lospec.com
  - [Hypernova 5](https://lospec.com/palette-list/hypernova-5) AKA Anemo by Isa on lospec.com
  - [Neon Moon Tarot](https://lospec.com/palette-list/neon-moon-tarot) AKA Electro by Interprete-me on lospec.com
  - [Koukasita](https://lospec.com/palette-list/koukasita) AKA Geo by namida on lospec.com

+ *(Previously used)*
  - [PyQt5](https://pypi.org/project/PyQt5/) for creating an open source easy-to-use framework.
  - [Playsound](https://pypi.org/project/playsound/1.2.2/) for creating a cross platform module to easily play sound files.
  - [Itemize](https://freesound.org/people/Scrampunk/sounds/345297/) for creating this sound that is used for notifications
  - [Apprise](https://pypi.org/project/apprise/) for creating an all-in-one notification module.
  - [Win10Toast](https://pypi.org/project/win10toast/) for creating an easy way to implement windows notifications.
