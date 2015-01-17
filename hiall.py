import RPi.GPIO as GPIO
import time
import ledmulti as led

while 1:
	for i in range(500):
		led.displayChar('H',2,False)
		time.sleep(0.002)
		led.displayChar('I',3,False)
		time.sleep(0.002)
	for j in range(333):
		led.displayChar('A',2,False)
		time.sleep(0.002)
		led.displayChar('L',3,False)
		time.sleep(0.002)
		led.displayChar('L',4,False)
		time.sleep(0.002)

GPIO.cleanup()
