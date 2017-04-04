import time
import RPi.GPIO as GPIO

print('Initializing LED.')
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
p=GPIO.PWM(7,500)
p.start(100)
print('ahoj')
try:
	print('go')
	while 1:
		for dc in range(0,101,5):
			print('up')
			p.ChangeDutyCycle(dc)
			time.sleep(0.1)
		for dc in range(100,-1,-5):
			print('down')
			p.ChangeDutyCycle(dc)
			time.sleep(0.1)
except KeyboardInterrupt:
	pass
p.stop()
GPIO.cleanup()
