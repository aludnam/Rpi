import ids, time
import RPi.GPIO as GPIO

Nc=10 #number of cycles
Nt=1 	#number of acquisition within each cycle

wait_time_s = 20#in s
exposure = 10 #in ms
name_template1 = 'cam1_cycle%03d_t%03d.png'
name_template2 = 'cam2_cycle%03d_t%03d.png'

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
n=0
while n<Nc:
	start=time.clock()
	p.ChangeDutyCycle(LED_on)
	time.sleep(1)
	cam1 = ids.Camera()
	cam1.color_mode = ids.ids_core.COLOR_MONO_8 
	cam1.exposure = exposure #in ms
	cam2 = ids.Camera()
	cam2.color_mode = ids.ids_core.COLOR_MONO_8 
	cam2.exposure = exposure #in ms
	ft = ids.ids_core.FILETYPE_PNG
	cam1.continuous_capture = True
	for t in range(Nt):		
		filename1=name_template1%(n,t)
		print('%d/%d %s'%(n*Nt+t+1,Nc*Nt,filename1))	
		for i in range(3): # first and second image are sometimes compromised
			cam1.next_save(filename1,filetype=ft,quality=100)
		time.sleep(1)
	time.sleep(2)
	cam1.continuous_capture = False
	del(cam1)
	cam2.continuous_capture = True
	for t in range(Nt):		
		filename2=name_template2%(n,t)
		print('%d/%d %s'%(n*Nt+t+1,Nc*Nt,filename2))	
		for i in range(3): # first and second image are sometimes compromised
			cam2.next_save(filename2,filetype=ft,quality=100)		
		time.sleep(1)
	del cam2
	time.sleep(2)
	p.ChangeDutyCycle(LED_off)
	n+=1
	finish=time.clock()
	wait=max(wait_time_s-(finish-start),0)
	print('Waiting %d sec.'%wait)
	time.sleep(wait)
	
raw_input('Acquisition finished. Press ENTER and unplug LED.')
p.stop()
GPIO.cleanup()
