from PIL import Image
import glob

images = glob.glob(r'C:\Temp\Timelapse\NGIF-9-12-21\Left\14h25min37s-26min57s\*.png')

l = 40
t = 0
r = 680
b = 480

i = 0

for image in images:
    im = Image.open(image)
    im1 = im.crop((l, t, r, b))
    print(im1.size)
    im1.save('C:/Temp/Timelapse/NGIF-9-12-21/Left/cropped/%s.png' %i)
    i += 1
    
    

#im1 = im.crop((l, t, r, b))

#im1.show()

#print(im1.size)