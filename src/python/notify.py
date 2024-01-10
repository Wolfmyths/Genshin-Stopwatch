from datetime import datetime

import PySide6.QtWidgets as qtw

from widgets.sysTrayIcon import sysTrayIcon

from saveConfig import saveConfig
from dataParser import dataParser, StopwatchDataKeys
from constants import TimeFormats

def Notify(title: str, message: str) -> None:
    sysTray: sysTrayIcon = qtw.QApplication.instance().findChild(sysTrayIcon)

    if sysTray.supportsMessages():
        sysTray.showMessage(title, message)

def checkMissedNotify() -> None:
    ''' 
    Checks for missed notifications
    for both stopwatches and static timers
    '''

    notificationsMissed: list[str] = []

    save = saveConfig()
    # If notifications are disabled, don't bother executing the rest
    if not save.getDesktopNotifications(): return
    stopwatches = dataParser()

    today = datetime.today().replace(microsecond=0)

    # stopwatches
    for stopwatch in stopwatches.sections():
        try:
            finishedDate = datetime.strptime(stopwatches.get(stopwatch, StopwatchDataKeys.time_finished), TimeFormats.Saved_Date)
        except Exception as e:
            print(f'Something went wrong converting a stopwatch finished date into a datetime object: {e}')
            continue

        if finishedDate <= today:
            notificationsMissed.append(stopwatches.get(stopwatch, StopwatchDataKeys.time_object))

    # static timers
    # daily reset
    if save.getDailyReset():
        dailyDeadline = save.getDailyDeadline()

        # If time has passed the static timer's deadline and if the notification settings are set to true
        if dailyDeadline <= today:
            notificationsMissed.append('Daily Reset')
    
    # weekly reset
    if save.getWeeklyReset():
        weeklyDeadline = save.getWeeklyDeadline()

        # If time has passed the static timer's deadline and if the notification settings are set to true
        if weeklyDeadline <= today:
            notificationsMissed.append('Weekly Reset')

    if notificationsMissed:
        Notify('Notifications were missed!', ', '.join(notificationsMissed))
