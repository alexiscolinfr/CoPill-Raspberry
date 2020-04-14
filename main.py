from connectionManager import *
from raspberryConfiguration import *
import argparse
from datetime import datetime,timedelta

def update(pillsList):

    with ConnectionManager() as db:

        #MONDAY
        mondayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%MONDAY%'")
        if len(mondayHours)>0:
            mondayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'monday'")
            logTime = datetimeToTimedelta(mondayLogHour[0][0])
            pillsList[0] = getPillsHours(mondayHours,logTime)

        #TUESDAY
        tuesdayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%TUESDAY%'")
        if len(tuesdayHours)>0:
            tuesdayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'tuesday'")
            logTime = datetimeToTimedelta(tuesdayLogHour[0][0])
            pillsList[1] = getPillsHours(tuesdayHours,logTime)

        #WEDNESDAY
        wednesdayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%WEDNESDAY%'")
        if len(wednesdayHours)>0:
            wednesdayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'wednesday'")
            logTime = datetimeToTimedelta(wednesdayLogHour[0][0])
            pillsList[2] = getPillsHours(wednesdayHours,logTime)

        #THURSDAY
        thursdayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%THURSDAY%'")
        if len(thursdayHours)>0:
            thursdayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'thursday'")
            logTime = datetimeToTimedelta(thursdayLogHour[0][0])
            pillsList[3] = getPillsHours(thursdayHours,logTime)

        #FRIDAY
        fridayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%FRIDAY%'")
        if len(fridayHours)>0:
            fridayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'friday'")
            logTime = datetimeToTimedelta(fridayLogHour[0][0])
            pillsList[4] = getPillsHours(fridayHours,logTime)

        #SATURDAY
        saturdayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%SATURDAY%'")
        if len(saturdayHours)>0:
            saturdayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'saturday'")
            logTime = datetimeToTimedelta(saturdayLogHour[0][0])
            pillsList[5] = getPillsHours(saturdayHours,logTime)

        #SUNDAY
        sundayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%SUNDAY%'")
        if len(sundayHours)>0:
            sundayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'sunday'")
            logTime = datetimeToTimedelta(sundayLogHour[0][0])
            pillsList[6] = getPillsHours(sundayHours,logTime)

    now = datetimeToTimedelta(datetime.now())
    setLedsColor(pillsList,now)

    return pillsList

def datetimeToTimedelta(datetime):
    return  timedelta(hours=datetime.hour, minutes=datetime.minute, seconds=datetime.second)

def getPillsHours(dayHours,dayLogTime):
    now = datetimeToTimedelta(datetime.now())
    result = []
    for hour in dayHours:
        if dayLogTime <  hour[0]:
            result.append(hour[0])
    return sorted(result)

def save_log(day):
    timestamp = datetime.now()
    with ConnectionManager() as db:
        db.execute('UPDATE log SET timestamp=%s WHERE day=%s',(timestamp,day))
    print ('log saved')

def notification_checks(pillsList):
    now = datetimeToTimedelta(datetime.now())
    weekday = datetime.now().weekday()
    for pillHour in pillsList[weekday]:
        if (now == pillHour):
            notification(weekday+1,"You have a pill to take!")

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    print ('--- CoPill box started ---')
    if not args.clear:
        print('Use "-c" argument to clear LEDs and OLED Display on exit')

    loadscreen()

    pillsList = [[],[],[],[],[],[],[]]

    try:

        pillsList = update(pillsList)

        while True:

            notification_checks(pillsList)

            if GPIO.input(TOUCH_PIN_1) == GPIO.HIGH:
                if len(pillsList[0])>0:
                    validation(1,'Monday\'s '+str(pillsList[0][0])+' pill was taken')
                    pillsList[0].pop(0)
                    save_log('monday')

            if GPIO.input(TOUCH_PIN_2) == GPIO.HIGH:
                if len(pillsList[1])>0:
                    validation(2,'Tuesday\'s '+str(pillsList[1][0])+' pill was taken')
                    pillsList[1].pop(0)
                    save_log('tuesday')

            if GPIO.input(TOUCH_PIN_3) == GPIO.HIGH:
                if len(pillsList[2])>0:
                    validation(3,'Wednesday\'s '+str(pillsList[2][0])+' pill was taken')
                    pillsList[2].pop(0)
                    save_log('wednesday')

            if GPIO.input(TOUCH_PIN_4) == GPIO.HIGH:
                if len(pillsList[3])>0:
                    validation(4,'Thursday\'s '+str(pillsList[3][0])+' pill was taken')
                    pillsList[3].pop(0)
                    save_log('thursday')

            if GPIO.input(TOUCH_PIN_5) == GPIO.HIGH:
                if len(pillsList[4])>0:
                    validation(5,'Friday\'s '+str(pillsList[4][0])+' pill was taken')
                    pillsList[4].pop(0)
                    save_log('friday')

            if GPIO.input(TOUCH_PIN_6) == GPIO.HIGH:
                if len(pillsList[5])>0:
                    validation(6,'Saturday\'s '+str(pillsList[5][0])+' pill was taken')
                    pillsList[5].pop(0)
                    save_log('saturday')

            if GPIO.input(TOUCH_PIN_7) == GPIO.HIGH:
                if len(pillsList[6])>0:
                    validation(7,'Sunday\'s '+str(pillsList[6][0])+' pill was taken')
                    pillsList[6].pop(0)
                    save_log('sunday')

            if GPIO.input(BUTTON_PIN_1) == GPIO.HIGH:
                pillsList = update(pillsList)
                loadscreen()

            if GPIO.input(BUTTON_PIN_2) == GPIO.HIGH:
                setAllLedColor(WHITE)
                clearscreen()

    except KeyboardInterrupt:
        if args.clear:
            setAllLedColor(WHITE)
            clearscreen()
            print ('--- CoPill box stopped ---')
