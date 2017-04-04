import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
Rpin = 37
UVpin = 32
GPIO.setup(Rpin,GPIO.OUT)
GPIO.setup(UVpin,GPIO.OUT)
red=GPIO.PWM(Rpin,500)
uv=GPIO.PWM(UVpin,500)

red_on = 0
red_off = 100
uv_on = 100
uv_off = 0
red.start(red_off)
uv.start(uv_off)

i=1
onoff_str = 'OFF','ON'
try:
	while 1:
		d=divmod(i,2)[1]
		color = raw_input('Press ENTER to turn the LED %s'%onoff_str[d])		
		if color.lower() == 'r':
			red.ChangeDutyCycle(d*100)
		elif color.lower() == 'u':
			uv.ChangeDutyCycle(d*100)			
		i+=1
except KeyboardInterrupt:
	pass
red.stop()
uv.stop()
GPIO.cleanup()

