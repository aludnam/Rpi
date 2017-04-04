import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32,GPIO.OUT)
p=GPIO.PWM(32,500)
p.start(0)

i=1
onoff_str = 'OFF','ON'
try:
	while 1:
		d=divmod(i,2)[1]
		raw_input('Press ENTER to turn the LED %s'%onoff_str[d])		
		p.ChangeDutyCycle(d*100)
		i+=1
except KeyboardInterrupt:
	pass
p.stop()
GPIO.cleanup()

