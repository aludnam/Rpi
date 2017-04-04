import ids, time, os
import RPi.GPIO as GPIO

Nc=15 #number of cycles
Nt=1 	#number of acquisition within each cycle

wait_time_s = 20#in s
exposure = 13 #in ms
name_template = 'cycle%03d_t%03d.png'
ft = ids.ids_core.FILETYPE_PNG

print('Initializing LED.')
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)
p=GPIO.PWM(37,500)
#p.start(100) #for some reason it has to be after init of camera...?

print('Initializing camera.')

print('%d cycles with %d s between cycles. Each cycle %d frames.'%(Nc,wait_time_s,Nt))
print('Total number of acquisition %d (%.2f hours).'%(Nc*Nt,Nc*Nt*wait_time_s/3600.))
print('Exposure time %d ms.'%exposure)
LED_on=0
LED_off=100
p.start(LED_off)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '/sys/bus/w1/devices/28-000008b67f21/w1_slave'
temp_log = 'temp_log.txt'

def temp_raw():
	f=open(temp_sensor,'r')
	lines = f.readlines()
	f.close()
	return lines
	
def read_temp():
	lines = temp_raw()
	while lines[0].strip()[-3:]!='YES':
		time.sleep(0.2)
		lines = temp_raw()
	temp_output = lines[1].find('t=')
		
	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string)/1000.0
		return temp_c

n=0
while n<Nc:
	start=time.clock()
	p.ChangeDutyCycle(LED_on)
	time.sleep(1)
	
	cam1 = ids.Camera()
	serial_num1 = cam1.info['serial_num']
	if not os.path.exists(serial_num1):
		os.makedirs(serial_num1)
	cam1.color_mode = ids.ids_core.COLOR_MONO_8 
	cam1.exposure = exposure #in ms
	
	cam2 = ids.Camera()
	serial_num2 = cam2.info['serial_num']
	if not os.path.exists(serial_num2):
		os.makedirs(serial_num2)
	cam2.color_mode = ids.ids_core.COLOR_MONO_8 
	cam2.exposure = exposure #in ms
	
	cam1.continuous_capture = True
	for t in range(Nt):		
		filename1=serial_num1 + '/' + name_template%(n,t)
		print('%d/%d %s'%(n*Nt+t+1,Nc*Nt,filename1))	
		for i in range(3): # first and second image are sometimes compromised
			cam1.next_save(filename1,filetype=ft,quality=100)
		time.sleep(1)
	time.sleep(2)
	cam1.continuous_capture = False
	del(cam1)
	
	cam2.continuous_capture = True
	for t in range(Nt):		
		filename2=serial_num2 + '/' + name_template%(n,t)
		print('%d/%d %s'%(n*Nt+t+1,Nc*Nt,filename2))	
		for i in range(3): # first and second image are sometimes compromised
			cam2.next_save(filename2,filetype=ft,quality=100)		
		time.sleep(1)
	del cam2
	
	time.sleep(2)
	p.ChangeDutyCycle(LED_off)
	datetemp =  '%s '%(name_template%(n,t)) + time.strftime("%c") + ' T=%s'%read_temp()
	print(datetemp)
	f=open(temp_log,'a')
	f.write(datetemp +'\n')
	f.close()
	n+=1
	finish=time.clock()
	wait=max(wait_time_s-(finish-start),0)
	print('Waiting %d sec.'%wait)
	time.sleep(wait)
	
raw_input('Acquisition finished. Press ENTER and unplug LED.')
p.stop()
GPIO.cleanup()
