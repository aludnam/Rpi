import ids, time
import RPi.GPIO as GPIO

Nc=5 #number of cycles
Nt=1 	#number of acquisition within each cycle

wait_time_s = 7 #in s
exposure = 30 #in ms
name_template = 'cycle%03d_t%03d.png'

print('Initializing LED.')
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)
p=GPIO.PWM(37,500)
#p.start(100) #for some reason it has to be after init of camera...?

print('Initializing camera.')

print('%d cycles with %d s between cycles. Each cycle %d frames.'%(Nc,wait_time_s,Nt))
print('Total number of acquisition %d (%.2f hours).'%(Nc*Nt,Nc*Nt*wait_time_s/3600.))
print('Exposure time %d ms.'%exposure)

on = 100
off = 0
p.start(off)
n=0
while n<Nc:
	start=time.clock()
	time.sleep(1)
	cam = ids.Camera()
	cam.color_mode = ids.ids_core.COLOR_MONO_8 
	cam.exposure = exposure #in ms
	ft = ids.ids_core.FILETYPE_PNG
	cam.continuous_capture = True
	time.sleep(2)
	p.ChangeDutyCycle(on)

	for t in range(Nt):		
		filename=name_template%(n,t)
		cam.next_save(filename,filetype=ft,quality=100) # first two images often corrupted... a bug?
		cam.next_save(filename,filetype=ft,quality=100)
		print('%d/%d %s'%(n*Nt+t+1,Nc*Nt,filename))	
		cam.next_save(filename,filetype=ft,quality=100)
		time.sleep(1)
	del cam
	p.ChangeDutyCycle(off)
	n+=1
	finish=time.clock()
	wait=max(wait_time_s-(finish-start),0)
	print('Waiting %d sec.'%wait)
	time.sleep(wait)
	
raw_input('Acquisition finished. Press ENTER and unplug LED.')
p.stop()
GPIO.cleanup()

