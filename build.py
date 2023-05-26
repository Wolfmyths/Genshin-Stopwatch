"""
This is a build file that is completely seperate to the main codebase.
It is responsible for compiling the program for each platform.
"""

import sys

import PyInstaller.__main__

# allows specification of platforms
args: list[str] = sys.argv

match len(args):
    case 0:
        print("No python option specified: args is null")
        sys.exit(1)
    case 1:
        print("No distribution option specified.")
        sys.exit(1)
    case 2:
        if args[1] == "--dist":
            print("No python distriution specified after --dist")
            sys.exit(1)
        print(f"Unknown argument: {args[1]}")
        sys.exit(1)
    case 3:
        if args[1] != "--dist":
            print(f"Unknown argument: {args[1]}")
            sys.exit(1)
        match args[2]:
            case "linux":
                PyInstaller.__main__.run(
                    ["main.py", "--strip", "--onefile", "--upx-dir=/usr/local/share/"]
                )
