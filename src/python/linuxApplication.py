from PySide6.QtCore import QObject
from constants import VERSION, LINUX_ICON
import desktop_entry_lib, sys, os, shutil

class setApplication(QObject):
    
        
    def buildApplication(self):
        iconPath = os.path.join(self.home, ".local", "share", "icons", "GenshinStopwatch.png")
        shutil.copyfile(LINUX_ICON, iconPath)
        newEntry = desktop_entry_lib.DesktopEntry()

        newEntry.Name.default_text = "Genshin Stopwatch"
        newEntry.Icon = iconPath
        newEntry.Comment.default_text = f"Genshin Stopwatch for Linux V{VERSION}"
        newEntry.Type = "Application"
        newEntry.Exec = sys.executable

        newEntry.write_file(self.entryPath)

    def validateApplication(self):
        currentEntry = desktop_entry_lib.DesktopEntry().from_file(self.entryPath)
        if currentEntry.Comment.default_text != f"Genshin Stopwatch for Linux V{VERSION}":
            os.remove(self.entryPath)
            self.buildApplication()
        if currentEntry.Exec != sys.executable:
            os.remove(self.entryPath)
            self.buildApplication()
        
    
    def __init__(self) -> None:
        super().__init__()
        self.home = os.path.expanduser("~")
        localIcons = os.path.join(self.home, ".local", "share", "icons")
        localApplications = os.path.join(self.home, ".local", "share", "applications")
        self.entryPath = os.path.join(self.home, ".local", "share", "applications", "Genshin Stopwatch.desktop")
        
        if os.path.exists(localIcons) == False:
            os.makedirs(localIcons)
        if os.path.exists(localApplications) == False:
            os.makedirs(localApplications)
        
        if os.path.exists(self.entryPath):
            self.validateApplication()
        else:
            self.buildApplication()