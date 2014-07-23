from PIL import Image
import numpy
import pdb

#name = raw_input("Filename: ")
image = Image.open("shred.jpg")
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
num_columns = width/shred_width

#calculates the magnitude difference of two 24bit pixels
#does not consider alpha
def getMagnitude(p1, p2):
        return ( (p1[0] - p2[0])**2 +(p1[1] - p2[1])**2 +(p1[2] - p2[2])**2 )**0.5
        #return ( (p1[0] - p2[0])**2 +(p1[1] - p2[2])**2 +(p1[2] - p2[2])**2 +(p1[3] - p2[3])**2)**0.5

#compares the left edge of a region with the right edge of another
def getError(region1, region2):
    err=0
    left_edge = numpy.asarray(region1.crop((shred_width-1, 0, shred_width, height)))
    left_edge = left_edge.astype(numpy.float64, copy=False)
    right_edge = numpy.asarray(region2.crop((0, 0, 1, height)))
    right_edge = right_edge.astype(numpy.float64, copy=False)
    diff = numpy.subtract(left_edge, right_edge)
    magnitude = numpy.sqrt(numpy.einsum('...i,...i', diff, diff))
    return magnitude.sum()



#keep track of the shredded parts for later reassembly        
unshredded = Image.new("RGBA", image.size)
shredList = []
for x in range(0, num_columns):
    x1, y1 = shred_width * x, 0
    x2, y2 = x1 + shred_width, height
    shredList.append(image.crop((x1, y1, x2, y2)))

leftTrack = range(num_columns)
rightTrack = range(num_columns)

#function uses vector difference to determine closeness between 2 strips
matches = []
minDiff = float("inf")
first = 0
end=-1
def findMatch(x):
    mini=float("inf")
    ind = -1
    mini2=float("inf")
    ind2 = -1
    for y in range(0, num_columns):
        if(x==y):
            continue
        val = getError(shredList[x], shredList[y])
        if(val< mini):
            mini=val
            ind = y

        val2 = getError(shredList[y], shredList[x])
        if(val2< mini2):
            mini2=val2
            ind2 = y
    return ind, ind2

#determine what strips are orphaned
for x in range(0, num_columns):
    indicies  = findMatch(x)
    matches.append(findMatch(x))
    if(indicies[0] in leftTrack):
       leftTrack.remove(indicies[0])
    if(indicies[1] in rightTrack):
       rightTrack.remove(indicies[1])

#find strips which are not common to both
for i in leftTrack[:]:
    if i in rightTrack:
        leftTrack.remove(i)
        rightTrack.remove(i)

#if its a left strip, it is the beginning, if right, it is pointing to the beginning
if(len(leftTrack)==1):
   newInd = leftTrack.pop()
elif(len(rightTrack)==1):
   newInd= matches[rightTrack.pop()][0]
else:
   exit()

#reassemble the image
newList = []
for x in range(0, num_columns):
   newList.append(shredList[newInd])
   newInd= matches[newInd][0]

destination_point = (0, 0)
for x in range(0, num_columns):
   destination_point = (x*shred_width, 0)
   unshredded.paste(newList[x], destination_point)
   


# Output the new image
unshredded.save("unshredded.jpg", "JPEG")
