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
            pillsList[0] = pillsVerification(mondayHours,logTime)
        else:
            pillsList[0]='no'

        #TUESDAY
        tuesdayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%TUESDAY%'")
        if len(tuesdayHours)>0:
            tuesdayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'tuesday'")
            logTime = datetimeToTimedelta(tuesdayLogHour[0][0])
            pillsList[1] = pillsVerification(tuesdayHours,logTime)
        else:
            pillsList[1]='no'

        #WEDNESDAY
        wednesdayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%WEDNESDAY%'")
        if len(wednesdayHours)>0:
            wednesdayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'wednesday'")
            logTime = datetimeToTimedelta(wednesdayLogHour[0][0])
            pillsList[2] = pillsVerification(wednesdayHours,logTime)
        else:
            pillsList[2]='no'

        #THURSDAY
        thursdayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%THURSDAY%'")
        if len(thursdayHours)>0:
            thursdayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'thursday'")
            logTime = datetimeToTimedelta(thursdayLogHour[0][0])
            pillsList[3] = pillsVerification(thursdayHours,logTime)
        else:
            pillsList[3]='no'

        #FRIDAY
        fridayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%FRIDAY%'")
        if len(fridayHours)>0:
            fridayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'friday'")
            logTime = datetimeToTimedelta(fridayLogHour[0][0])
            pillsList[4] = pillsVerification(fridayHours,logTime)
        else:
            pillsList[4]='no'

        #SATURDAY
        saturdayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%SATURDAY%'")
        if len(saturdayHours)>0:
            saturdayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'saturday'")
            logTime = datetimeToTimedelta(saturdayLogHour[0][0])
            pillsList[5] = pillsVerification(saturdayHours,logTime)
        else:
            pillsList[5]='no'

        #SUNDAY
        sundayHours = db.query("SELECT hour FROM treatment WHERE days LIKE '%SUNDAY%'")
        if len(sundayHours)>0:
            sundayLogHour = db.query("SELECT timestamp FROM log WHERE day = 'sunday'")
            logTime = datetimeToTimedelta(sundayLogHour[0][0])
            pillsList[6] = pillsVerification(sundayHours,logTime)
        else:
            pillsList[6]='no'

    setLedsColor(pillsList)

    return pillsList

def datetimeToTimedelta(datetime):
    return  timedelta(hours=datetime.hour, minutes=datetime.minute, seconds=datetime.second)

def pillsVerification(dayHours,dayLogTime):
    now = datetimeToTimedelta(datetime.now())
    upToDate = True
    result = None
    for hour in dayHours:
        if dayLogTime <  hour[0] and hour[0] < now:
            upToDate = False
            break
    if upToDate:
        result='no'
    else:
        result='yes'
    return result

def save_log(day):
    timestamp = datetime.now()
    with ConnectionManager() as db:
        db.execute('UPDATE log SET timestamp=%s WHERE day=%s',(timestamp,day))
    print ('log saved')

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    print ('--- CoPill box started ---')
    if not args.clear:
        print('Use "-c" argument to clear LEDs and OLED Display on exit')

    loadscreen()

    pillsList = ['no']*7

    try:

        pillsList = update(pillsList)

        while True:

            if GPIO.input(TOUCH_PIN_1) == GPIO.HIGH:
                if pillsList[0] == 'yes':
                    pillsList[0] = 'no'
                    validation(1,'Monday pills were taken')
                    save_log('monday')

            if GPIO.input(TOUCH_PIN_2) == GPIO.HIGH:
                if pillsList[1] == 'yes':
                    pillsList[1] = 'no'
                    validation(2,'Tuesday pills were taken')
                    save_log('tuesday')

            if GPIO.input(TOUCH_PIN_3) == GPIO.HIGH:
                if pillsList[2] == 'yes':
                    pillsList[2] = 'no'
                    validation(3,'Wednesday pills were taken')
                    save_log('wednesday')

            if GPIO.input(TOUCH_PIN_4) == GPIO.HIGH:
                if pillsList[3] == 'yes':
                    pillsList[3] = 'no'
                    validation(4,'Thursday pills were taken')
                    save_log('thursday')

            if GPIO.input(TOUCH_PIN_5) == GPIO.HIGH:
                if pillsList[4] == 'yes':
                    pillsList[4] = 'no'
                    validation(5,'Friday pills were taken')
                    save_log('friday')

            if GPIO.input(TOUCH_PIN_6) == GPIO.HIGH:
                if pillsList[5] == 'yes':
                    pillsList[5] = 'no'
                    validation(6,'Saturday pills were taken')
                    save_log('saturday')

            if GPIO.input(TOUCH_PIN_7) == GPIO.HIGH:
                if pillsList[6] == 'yes':
                    pillsList[6] = 'no'
                    validation(7,'Sunday pills were taken')
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
