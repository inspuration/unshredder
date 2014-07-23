from PIL import Image
import random
image = Image.open("scragl.jpg")
data = image.getdata() # This gets pixel data

# Access an arbitrary pixel. Data is stored as a 2d array where rows are
# sequential. Each element in the array is a RGBA tuple (red, green, blue,
# alpha).

x, y = 20, 90
def get_pixel_value(x, y):
   width, height = image.size
   pixel = data[y * width + x]
   return pixel
print get_pixel_value(20, 30)

# Create a new image of the same size as the original
# and copy a region into the new image
shred_width = 32
width  = image.size[0]
height = image.size[1]
unshredded = Image.new("RGBA", image.size)

shredList = []

for x in range(0, width/shred_width):
    x1, y1 = shred_width * x, 0
    x2, y2 = x1 + shred_width, height
    shredList.append(image.crop((x1, y1, x2, y2)))

random.shuffle(shredList)

x=0
while shredList:
   source = shredList.pop()
   destination_point = (x*shred_width, 0)
   unshredded.paste(source, destination_point)
   x+=1
   

# Output the new image
unshredded.save("myshred3.jpg", "JPEG")
