from connectionManager import *
from raspberryConfiguration import *
import argparse
from datetime import datetime

def update(pillsList):
    with ConnectionManager() as db:

        monday = db.query("SELECT id FROM treatment WHERE days LIKE '%MONDAY%'")
        if len(monday)>0:
            pillsList[0]='yes'
            setLedColor(1,RED)
        else:
            setLedColor(1,GREEN)

        tuesday = db.query("SELECT id FROM treatment WHERE days LIKE '%TUESDAY%'")
        if len(tuesday)>0:
            pillsList[1]='yes'
            setLedColor(2,RED)
        else:
            setLedColor(2,GREEN)

        wednesday = db.query("SELECT id FROM treatment WHERE days LIKE '%WEDNESDAY%'")
        if len(wednesday)>0:
            pillsList[2]='yes'
            setLedColor(3,RED)
        else:
            setLedColor(3,GREEN)

        thursday = db.query("SELECT id FROM treatment WHERE days LIKE '%THURSDAY%'")
        if len(thursday)>0:
            pillsList[3]='yes'
            setLedColor(4,RED)
        else:
            setLedColor(4,GREEN)

        friday = db.query("SELECT id FROM treatment WHERE days LIKE '%FRIDAY%'")
        if len(friday)>0:
            pillsList[4]='yes'
            setLedColor(5,RED)
        else:
            setLedColor(5,GREEN)

        saturday = db.query("SELECT id FROM treatment WHERE days LIKE '%SATURDAY%'")
        if len(saturday)>0:
            pillsList[5]='yes'
            setLedColor(6,RED)
        else:
            setLedColor(6,GREEN)

        sunday = db.query("SELECT id FROM treatment WHERE days LIKE '%SUNDAY%'")
        if len(sunday)>0:
            pillsList[6]='yes'
            setLedColor(7,RED)
        else:
            setLedColor(7,GREEN)

    return pillsList

def save_log(day):
    timestamp = datetime.now()
    with ConnectionManager() as db:
        db.execute('INSERT INTO log (id, day, timestamp) VALUES (null, %s, %s)',(day,timestamp))
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
                    print ('Monday pills were taken')
                    pillsList[0] = 'no'
                    validation(1)
                    save_log('monday')

            if GPIO.input(TOUCH_PIN_2) == GPIO.HIGH:
                if pillsList[1] == 'yes':
                    print ('Tuesday pills were taken')
                    pillsList[1] = 'no'
                    validation(2)
                    save_log('tuesday')

            if GPIO.input(TOUCH_PIN_3) == GPIO.HIGH:
                if pillsList[2] == 'yes':
                    print ('Wednesday pills were taken')
                    pillsList[2] = 'no'
                    validation(3)
                    save_log('wednesday')

            if GPIO.input(TOUCH_PIN_4) == GPIO.HIGH:
                if pillsList[3] == 'yes':
                    print ('Thursday pills were taken')
                    pillsList[3] = 'no'
                    validation(4)
                    save_log('thursday')

            if GPIO.input(TOUCH_PIN_5) == GPIO.HIGH:
                if pillsList[4] == 'yes':
                    print ('Friday pills were taken')
                    pillsList[4] = 'no'
                    validation(5)
                    save_log('friday')

            if GPIO.input(TOUCH_PIN_6) == GPIO.HIGH:
                if pillsList[5] == 'yes':
                    print ('Saturday pills were taken')
                    pillsList[5] = 'no'
                    validation(6)
                    save_log('saturday')

            if GPIO.input(TOUCH_PIN_7) == GPIO.HIGH:
                if pillsList[6] == 'yes':
                    print ('Sunday pills were taken')
                    pillsList[6] = 'no'
                    validation(7)
                    save_log('sunday')

            if GPIO.input(BUTTON_PIN_1) == GPIO.HIGH:
                pillsList = update(pillsList)

            if GPIO.input(BUTTON_PIN_2) == GPIO.HIGH:
                setAllLedColor(WHITE)

    except KeyboardInterrupt:
        if args.clear:
            setAllLedColor(WHITE)
            clearscreen()
            print ('--- CoPill box stopped ---')
