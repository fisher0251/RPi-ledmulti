# ledmulti.py
# Library of functions for multiplexing a
# 4-digit 7-segment LED display
# by Dan Fisher, 2014-01-10
# last updated 2014-01-15

import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Time to flash each digit in display()
SLEEP_TIME = 0.002	# seconds

# Map GPIO pins to LED segments and digits
segments = {'A':23, 'B': 24, 'C': 12, 'D': 20, 'E': 21, 'F': 18, 'G': 25, 'DP': 16}
digits = {1: 22, 2: 4, 3: 19, 4: 6}

# Set GPIO pins for output, initialize to 0
for key in segments:
	GPIO.setup(segments[key], GPIO.OUT, initial=GPIO.LOW)
for key in digits:
	GPIO.setup(digits[key], GPIO.OUT, initial=GPIO.LOW)

# Displays a floating point value between 0 and 9999 inclusive on the display for 
# display_time in seconds with given number of decimal places 0-3
def display(number,decimals,display_time):
	# Check for acceptable arguments
	if display_time < 0:
		return
		
	if number < 0:
		number = 0
		decimals = 0
	elif number > 9999:
		number = 9999
		decimals = 0
	
	if decimals < 0:
		decimals = 0
	elif decimals > 3:
		decimals = 3
	
	# Stringify the number to be displayed with the correct number of 
	# decimals
	if decimals == 0:
		number_string = '{0:0.0f}'.format(number)
	elif decimals == 1:
		number_string = '{0:0.1f}'.format(number)
	elif decimals == 2:
		number_string = '{0:0.2f}'.format(number)
	elif decimals == 3:
		number_string = '{0:0.3f}'.format(number)
	
	# Add leading zeros and trailing decimal point so that number_string
	# has 5 characters
	if decimals == 0:
		while(len(number_string) < 4):
			number_string = '0' + number_string
		number_string = number_string + '.'  # Adds trailing decimal point
	else:
		while(len(number_string) < 5):
			number_string = '0' + number_string
	
	# If too many characters in number_string, lop of ending decimals until it
	# will fit on the LED display
	while len(number_string) > 5:
		number_string = number_string[0:len(number_string)-1]
	
	# Find which character the decimal point is in so it can be displayed later
	place = 0
	for i in range(5):
		if number_string[i] == '.':
				place = i
				
	# Slice out decimal so that each character can be sent to displayChar()
	number_string = number_string[0:place]+number_string[place+1:5]
	
	# Create a boolean array for where to display the decimal
	decimal_location = [False,False,False,False]
	for i in range(4):
		if (i + 1) == place:
			decimal_location[i] = True
		else:
			decimal_location[i] = False
	
	display_time *= 1e6		# Convert to microseconds
	t_start = datetime.now()
	delta_t_micros = 0
	# Keep multiplexing the display until display_time runs out
	while delta_t_micros < display_time:
		# Display digits
		for i in range(4):
			displayChar(number_string[i],i+1,decimal_location[i])
			time.sleep(SLEEP_TIME)
		
		delta_t = datetime.now() - t_start
		delta_t_micros = delta_t.seconds * 1e6 + delta_t.microseconds

	# Clear LED display
	for key in digits:	# Turn off all digits
		GPIO.output(digits[key], GPIO.LOW)
	for key in segments:	# Turn off all segments
		GPIO.output(segments[key],GPIO.LOW)
	return

# Displays the integer numbers 0-9 on digit 1 through 4 (left to right)
# decimal = True displays the decimal point on the given digit
# Also can display characters ABCDEFGHIJLOPSUY 
def displayChar(character, digit, decimal):
	for key in digits:	# Turn off all digits
		GPIO.output(digits[key], GPIO.LOW)
	for key in segments:	# Turn off all segments
		GPIO.output(segments[key],GPIO.LOW)
	
	# A font for displaying on a 7-segment display
	if character == '0':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
	elif character == '1':
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
	elif character == '2':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
	elif character == '3':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
	elif character == '4':
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
	elif character == '5':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
	elif character == '6':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
	elif character == '7':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
	elif character == '8':
		for key in segments:
			if key != 'DP':
				GPIO.output(segments[key],GPIO.HIGH)
	elif character == '9':
		for key in segments:
			if (key != 'DP') and (key != 'E'):
				GPIO.output(segments[key],GPIO.HIGH)
	elif character == 'A':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
	elif character == 'B':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
	elif character == 'C':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
	elif character == 'D' or character == 'O':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
	elif character == 'E':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
	elif character == 'F':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
	elif character == 'G':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
	elif character == 'H':
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
	elif character == 'I':
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
	elif character == 'J':
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
	elif character == 'L':
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
	elif character == 'P':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
	elif character == 'S':
		GPIO.output(segments['A'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
	elif character == 'U':
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['E'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
	elif character == 'Y':
		GPIO.output(segments['B'],GPIO.HIGH)
		GPIO.output(segments['C'],GPIO.HIGH)
		GPIO.output(segments['D'],GPIO.HIGH)
		GPIO.output(segments['F'],GPIO.HIGH)
		GPIO.output(segments['G'],GPIO.HIGH)
	else:
		return
		
	if decimal == True:
		GPIO.output(segments['DP'],GPIO.HIGH)
	
	# Turn on digit
	GPIO.output(digits[digit], GPIO.HIGH)
	return