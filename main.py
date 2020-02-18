from connectionManager import *
from raspberryConfiguration import *
import argparse

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    print ('--- CoPill box started ---')
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    strip = getStrip()
    pillsList = ['no']*7

    try:
        setAllLedColor(strip,GREEN)

        with ConnectionManager() as db:
            #db.execute('INSERT INTO comments (username, comment_body, date_posted) VALUES (?, ?, current_date)', ('tom', 'this is a comment'))
            monday = db.query("SELECT id FROM treatment WHERE days LIKE '%MONDAY%'")
            if len(monday)>0:
                pillsList[0]='yes'
                setLedColor(strip,1,RED)
            tuesday = db.query("SELECT id FROM treatment WHERE days LIKE '%TUESDAY%'")
            if len(tuesday)>0:
                pillsList[1]='yes'
                setLedColor(strip,2,RED)
            wednesday = db.query("SELECT id FROM treatment WHERE days LIKE '%WEDNESDAY%'")
            if len(wednesday)>0:
                pillsList[2]='yes'
                setLedColor(strip,3,RED)
            thursday = db.query("SELECT id FROM treatment WHERE days LIKE '%THURSDAY%'")
            if len(thursday)>0:
                pillsList[3]='yes'
                setLedColor(strip,4,RED)
            friday = db.query("SELECT id FROM treatment WHERE days LIKE '%FRIDAY%'")
            if len(friday)>0:
                pillsList[4]='yes'
                setLedColor(strip,5,RED)
            saturday = db.query("SELECT id FROM treatment WHERE days LIKE '%SATURDAY%'")
            if len(saturday)>0:
                pillsList[5]='yes'
                setLedColor(strip,6,RED)
            sunday = db.query("SELECT id FROM treatment WHERE days LIKE '%SUNDAY%'")
            if len(sunday)>0:
                pillsList[6]='yes'
                setLedColor(strip,7,RED)

        while True:

            if GPIO.input(TOUCH_PIN_1) == GPIO.HIGH:
                if pillsList[0] == 'yes':
                    print ('Monday pills were taken')
                    pillsList[0] = 'no'
                    validation(strip,1)

            if GPIO.input(TOUCH_PIN_2) == GPIO.HIGH:
                if pillsList[1] == 'yes':
                    print ('Tuesday pills were taken')
                    pillsList[1] = 'no'
                    validation(strip,2)

            if GPIO.input(TOUCH_PIN_3) == GPIO.HIGH:
                if pillsList[2] == 'yes':
                    print ('Wednesday pills were taken')
                    pillsList[2] = 'no'
                    validation(strip,3)

            if GPIO.input(TOUCH_PIN_4) == GPIO.HIGH:
                if pillsList[3] == 'yes':
                    print ('Thursday pills were taken')
                    pillsList[3] = 'no'
                    validation(strip,4)

            if GPIO.input(TOUCH_PIN_5) == GPIO.HIGH:
                if pillsList[4] == 'yes':
                    print ('Friday pills were taken')
                    pillsList[4] = 'no'
                    validation(strip,5)

            if GPIO.input(TOUCH_PIN_6) == GPIO.HIGH:
                if pillsList[5] == 'yes':
                    print ('Saturday pills were taken')
                    pillsList[5] = 'no'
                    validation(strip,6)

            if GPIO.input(TOUCH_PIN_7) == GPIO.HIGH:
                if pillsList[6] == 'yes':
                    print ('Sunday pills were taken')
                    pillsList[6] = 'no'
                    validation(strip,7)

            if GPIO.input(BUTTON_PIN_1) == GPIO.HIGH:
                setAllLedRandColor(strip)

            if GPIO.input(BUTTON_PIN_2) == GPIO.HIGH:
                setAllLedColor(strip,WHITE)

    except KeyboardInterrupt:
        if args.clear:
            setAllLedColor(strip,WHITE)
            print ('--- CoPill box stopped ---')
