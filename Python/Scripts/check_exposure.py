import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import ids
exposure = 3 #in ms
name_template = 'cycle%03d_t%03d.png'
cam = ids.Camera(handle = 1)
#cam.color_mode = ids.ids_core.COLOR_MONO_8 
cam.exposure = exposure #in ms
ft = ids.ids_core.FILETYPE_PNG
cam.continuous_capture = True

img, meta = cam.next()
img, meta = cam.next()
img, meta = cam.next()

if img.ndim > 2:
	img = img[:,:,0]

cent = (img.shape[0]/2, img.shape[1]/2)
avg = img.mean()

plt.ion()
plt.figure()
plt.imshow(img[cent[0]-128:cent[0]+127, cent[1]-128:cent[1]+127])
plt.title('Center ROI')
plt.show()

plt.figure()
a = plt.hist(img.ravel(), bins=256, range = (0,256))
plt.title('Histogram of intensities, mean = %d'%avg)
plt.xlabel('Intensity')
plt.ylabel('Counts')
plt.grid('on')
plt.xlim([0,256])
plt.show()

ideal_exposure = 128/avg*exposure
saturated = a[0][-1]
print('There are %d saturated pixels (%g percent).'%(saturated, saturated/img.size*100))
print('Ideal exposure is %d ms.'%(ideal_exposure))
raw_input('Press Enter to quit')
plt.close('all')
