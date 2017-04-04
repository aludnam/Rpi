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

i=0
onoff_str = 'ON','OFF', 'ON', 'OFF'
col_str = 'UV', 'UV', 'RED', 'RED'
try:
	while 1:
		d=divmod(i,4)[1]
		inpt = raw_input('Press ENTER to turn the %s LED %s ("q" to quit)'%(col_str[d],onoff_str[d]))		
		if d==0:
			uv.ChangeDutyCycle(uv_on)
		elif d==1:
			uv.ChangeDutyCycle(uv_off)
		elif d==2:
			red.ChangeDutyCycle(red_on)
		elif d==3:
			red.ChangeDutyCycle(red_off)			
		i+=1
		if 'q' in inpt.lower():
			break
except KeyboardInterrupt:
	pass
red.stop()
uv.stop()
GPIO.cleanup()

