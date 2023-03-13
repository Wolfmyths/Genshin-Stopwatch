# Genshin Stopwatch
### A program to help keep track of Genshin Impact's time gates. <img src="icon.png" width="150" height="150">

## What does Genshin Stopwatch do?

Genshin Stopwatch is a program that makes checking timers easier without launching the game (Examples: Stamina, Fishing, Gardening, Enemy Respawns, Parametric Transformer, etc...).

The only caviat is that you have to start the stopwatch yourself!

## How does it work?

Genshin Stopwatch is a program that is *does not require an internet connection* to use and *does not run in the background*. When you start up the program it will calculate the difference between when you started the program and when the destination of said timer is.

When you close the application your stopwatches will save to the `save.txt` file. The save file is easily configurable and easy to read.

Here is an example of a stopwatch's save data in `save.txt`:

> Name: Parametric Transformer<br>
> Time Finished: 2023-03-19 20:07:18<br>
> Time Original Duration: 168:00:00<br>
> Border Color: #37AA9C<br>
> Notes:<br>

## What platforms is this compatible with?

At the moment only Windows machines can run this program, I'm not sure if I plan on making mobile versions.

## It doesn't work!

+ Check `save.txt` and make sure it looks in a similar format to the example above.
+ The program needs `save.txt` to start, so if there isn't one in the directory create a text file with the same name.
+ Genshin Stopwatch only works on `Windows`.

If you found a bug or crash, please report it to me and show how to replicate the issue if possible.<br>
**Before submitting a bug report please check the known bugs in the release notes before telling me.**

## Future Plans?

+ Add windows notifications when a stopwatch finishes

If you have a suggestion let me know!

## Credits

Thanks to [PyQt5](https://pypi.org/project/PyQt5/) for making an open source easy-to-use framework.
