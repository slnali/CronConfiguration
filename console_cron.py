
import logging
import sys
from datetime import date, datetime, time, timedelta

TODAY = "today"
TOMORROW = "tomorrow"

#Given more time I would have added more error handling and catch more edge cases
#The input could also be sanitised to ensure we are getting what we expect

def getNearestTimeWhenCommandWillExecute(currentTime: str, configLine: str) -> str:
    nextPeriod = TODAY
    currentHour, currentMinute,  = currentTime.split(":")
    configMinute, configHour, command = configLine.split(" ")
    currentTime = time(int(currentHour), int(currentMinute))

    if configMinute == "*" and configHour == "*":
        nextDateTime = currentTime

    elif configMinute == "*":
        #do mins logic i.e. every minute at specific hour
        nextDateTime, nextPeriod = getNearestTimeForRunningCommandEveryMinuteAtSpecificHour(currentTime, configHour, nextPeriod)

    elif configHour == "*":
        #do hours logic i.e. every hour at specific minute
        configTime = time(int(currentHour),int(configMinute))
        nextDateTime, nextPeriod = getNearestTimeForRunningCommandEveryHourAtSpecificMinute(currentTime, configTime, nextPeriod)
    
    else:
        configTime = time(int(configHour),int(configMinute))
        nextDateTime, nextPeriod  = getNearestTimeForRunningCommandDaily(currentTime, configTime, nextPeriod)

    return "{nextDateTime} {nextPeriod} - {command}".format(nextDateTime = nextDateTime.strftime("%H:%M"),nextPeriod=nextPeriod,command=command)

def getNearestTimeForRunningCommandDaily(currentTime, configTime, nextPeriod):
    if currentTime > configTime:
        nextPeriod = TOMORROWde
    nextDateTime = configTime
    return nextDateTime, nextPeriod


def getNearestTimeForRunningCommandEveryHourAtSpecificMinute(currentTime, configTime, nextPeriod):
    if currentTime > configTime:
        dateTimeDifference = datetime.combine(date.today(), configTime) - datetime.combine(date.today(), currentTime)
        differenceInMinutes = divmod(dateTimeDifference.total_seconds(), 60)[0]
        #add the time difference to get next run time in next hour
        nextDateTime = datetime.combine(date.today(), currentTime) + timedelta(minutes=60+differenceInMinutes)
        if nextDateTime.day > date.today().day: 
            nextPeriod = TOMORROW
    else:
        nextDateTime = datetime.combine(date.today(), configTime)
    return nextDateTime, nextPeriod


def getNearestTimeForRunningCommandEveryMinuteAtSpecificHour(currentTime, configHour, nextPeriod):
    configTimeStart = time(int(configHour),int(0))
    configTimeEnd = time(int(configHour),int(59))
    if configTimeStart <= currentTime <= configTimeEnd:
        nextDateTime = currentTime
    else:
        if currentTime > configTimeEnd:
            nextPeriod = TOMORROW
        nextDateTime = configTimeStart
    return nextDateTime, nextPeriod


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    args = sys.argv
    if len(args) > 1:
        currentTime = args[1]
    else:
        logging.error("Error: Simulated time argument not passed in")
        sys.exit(1) 

    for line in sys.stdin:
        print(getNearestTimeWhenCommandWillExecute(currentTime, line.rstrip()))

    
