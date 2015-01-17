# displayexample.py
# Example program showing how to use the ledmulti library functions
# Dan Fisher, 2014-01-10
# updated 2014-01-15

import ledmulti as led
import time
import RPi.GPIO as GPIO

# Displays a number for display time in seconds, with up to 3 decimal places
# Segments all go off after display time is complete
# Example: display(number,decimals,display_time)
led.display(1234,0,3)
time.sleep(1)
led.display(432.1,1,3)
time.sleep(1)
led.display(2.12345,3,3)
time.sleep(1)

# Counting up from 0 to 100. Notice there is no need for a delay
# between displays since the display() function is timed already
for i in range(101):
	led.display(i,0,0.1)
time.sleep(1)

# Numbers that are too high default to 9999, and numbers that
# are too low (negative) default to 0
led.display(12500.55,2,3)
led.display(-500,0,3) 

# Good to do at the end of your program to shut off all the GPIO
# pins
GPIO.cleanup()
