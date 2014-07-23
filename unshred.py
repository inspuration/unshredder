from PIL import Image

#name = raw_input("Filename: ")
image = Image.open("myshred.jpg")
data = image.getdata() # This gets pixel data

# Access an arbitrary pixel. Data is stored as a 2d array where rows are
# sequential. Each element in the array is a RGBA tuple (red, green, blue,
# alpha).

def get_pixel_value(x, y):
   width, height = image.size
   pixel = data[y * width + x]
   return pixel

# Create a new image of the same size as the original
# and copy a region into the new image
shred_width = 32 #TODO: Bonus?
width = image.size[0]
height = image.size[1]

#calculates the magnitude difference of two 24bit pixels
#does not consider alpha
def getMagnitude(p1, p2):
        return ( (p1[0] - p2[0])**2 +(p1[1] - p2[1])**2 +(p1[2] - p2[2])**2 )**0.5
        #return ( (p1[0] - p2[0])**2 +(p1[1] - p2[2])**2 +(p1[2] - p2[2])**2 +(p1[3] - p2[3])**2)**0.5

#compares the left edge of a region with the right edge of another
def getError(region1, region2):
    err=0    
    for x in range(0, height):
        p1 = region1[shred_width-1, x]
        p2 = region2[0,x]
        err += getMagnitude(p1,p2)
    return err



        
unshredded = Image.new("RGBA", image.size)

shredList = []
repairList = []

for x in range(0, width/shred_width):
    x1, y1 = shred_width * x, 0
    x2, y2 = x1 + shred_width, height
    repairList.append(image.crop((x1, y1, x2, y2)))
    shredList.append(image.crop((x1, y1, x2, y2)).load())

leftMatch = []
minDiff = float("inf")
first = 0
for x in range(0, width/shred_width):
    mini=float("inf")
    ind = -1
    mini2=float("inf")
    averageError = 0
    for y in range(0, width/shred_width):
        if(x==y):
            continue
        val = getError(shredList[x], shredList[y])
        if(val< mini):
            mini=val
            ind = y
        val2 = getError(shredList[y], shredList[x])
        if(val2< mini2):
            mini2=val2
    if(minDiff > mini-mini2):
       minDiff = mini - mini2
       first = x
    print mini
    leftMatch.append(ind)



newList = []
newInd=first
for x in range(0, width/shred_width):
   newList.append(repairList[newInd])
   newInd=leftMatch[newInd]

destination_point = (0, 0)
for x in range(0, width/shred_width):
   destination_point = (x*shred_width, 0)
   unshredded.paste(newList[x], destination_point)
   


# Output the new image
unshredded.save("unshredded.jpg", "JPEG")
