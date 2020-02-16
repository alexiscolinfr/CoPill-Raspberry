import connectionManager
import argparse
import raspberryConfiguration

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    strip = getStrip()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
		with ConnectionManager() as db:
    		#db.execute('INSERT INTO comments (username, comment_body, date_posted) VALUES (?, ?, current_date)', ('tom', 'this is a comment'))
    		comments = db.query('SELECT * FROM user')
    		print(comments)

        print('Press a touch sensor')
        setAllLedColor(strip,RED)
        while True:

            if GPIO.input(TOUCH_PIN_1) == GPIO.HIGH:
                validation(strip,1)

            if GPIO.input(TOUCH_PIN_2) == GPIO.HIGH:
                validation(strip,2)

            if GPIO.input(TOUCH_PIN_3) == GPIO.HIGH:
                validation(strip,3)

            if GPIO.input(TOUCH_PIN_4) == GPIO.HIGH:
                validation(strip,4)

            if GPIO.input(TOUCH_PIN_5) == GPIO.HIGH:
                validation(strip,5)

            if GPIO.input(TOUCH_PIN_6) == GPIO.HIGH:
                validation(strip,6)

            if GPIO.input(TOUCH_PIN_7) == GPIO.HIGH:
                validation(strip,7)

            if GPIO.input(BUTTON_PIN_1) == GPIO.HIGH:
                setAllLedRandColor(strip)

            if GPIO.input(BUTTON_PIN_2) == GPIO.HIGH:
                setAllLedColor(strip,WHITE)

    except KeyboardInterrupt:
        if args.clear:
            setAllLedColor(strip,WHITE)