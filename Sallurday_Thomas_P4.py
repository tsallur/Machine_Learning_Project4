#Thomas Sallurday
#Professor Hodges
#CPSC 6430
#11-16-2020
import numpy as np
import matplotlib.pyplot as plot
import math 

#function used to calculate distance between points
def euclid_distance(x1,y1,x2,y2):
    part1 = (x2 - x1) * (x2 - x1)
    part2 = (y2 - y1) * (y2 - y1)
    part3 = part1 + part2
    part4 = math.sqrt(part3)
    return part4
#function that copies the 3rd column of a matrix. Used for keeping track of changing
#centroids
def arrayCopy(current,previous,rows):
    i = 0
    while(i < rows):
        previous[i][2] = current[i][2]
        i = i + 1
    return previous
#function that determines if the k means algorithm is finished
def checkEndState(current,previous,rows):
    i = 0
    numOfChanges = 0
    while(i < rows):
        if(current[i][2] != previous[i][2]):
            numOfChanges = numOfChanges + 1
        i = i + 1
    if(numOfChanges > 0):
        return False
    else:
        return True


dataFileName = input("Please enter the name of the Data file: ")

dataFile = open(dataFileName,'r')
dataLine = dataFile.readline()
dataLine = dataLine.split('\t')
rows = int(dataLine[0])
cols = int(dataLine[1])
ogData = np.zeros([rows,cols])
i = 0
j = 0
dataLine = dataFile.readline()
while(dataLine != ""):
    dataLine = dataLine.split('\t')
    j = 0;
    while(j < cols):
        ogData[i][j] = float(dataLine[j])
        j = j + 1
    i = i + 1
    dataLine = dataFile.readline()
dataFile.close()

centroidFileName = input("Please enter the name of the file that cotains the initial centroid information: ")

dataFile = open(centroidFileName,'r')
dataLine = dataFile.readline()
dataLine = dataLine.split('\n')
rows2 = int(dataLine[0])
centroids = np.zeros([rows2,cols])
i = 0
j = 0
dataLine = dataFile.readline()
while(dataLine != ""):
    dataLine = dataLine.split('\t')
    j = 0;
    while(j < cols):
        centroids[i][j] = float(dataLine[j])
        j = j + 1
    i = i + 1
    dataLine = dataFile.readline()
dataFile.close()
i = 1
j = 0
print()
plot1 = plot.figure(1)
while(i < rows2 + 1):
    print(" Initial Centroid" +str(i) + ": ")
    i = i + 1
    j = 0
    if(i == 2):
        plot.scatter(centroids[i-2][0],centroids[i-2][1], color = "red",marker = "*")
    else:
        plot.scatter(centroids[i-2][0],centroids[i-2][1], color = "green",marker = "*")
    while(j < cols):
        print("x" + str(j + 1) +": " + str(centroids[i-2][j]) + " "  )
        j = j + 1
i = 0
j = 0
while (i < rows):
    j = 0
    i = i + 1
    plot.scatter(ogData[i-1][0],ogData[i-1][1],color = "purple",marker = "o")
    
plot.xlabel("x1 Axis")
plot.ylabel("x2 Axis")
plot.title("Initial Data Points")
plot.savefig("Initial_Data_Points.png",bbox_inches = "tight")
i = 0;
currentData = np.zeros([rows,cols + 1])
previousData = np.zeros([rows,cols+ 1])
while(i < rows):
    distance1 = euclid_distance(centroids[0][0],centroids[0][1],ogData[i][0],ogData[i][1])
    distance2 = euclid_distance(centroids[1][0],centroids[1][1],ogData[i][0],ogData[i][1])
    if(distance1 < distance2):
        currentData[i][0] = ogData[i][0]
        previousData[i][0] = ogData[i][0]
        currentData[i][1] = ogData[i][1]
        previousData[i][1] = ogData[i][1]
        currentData[i][2] = 1
        
    else:
        currentData[i][0] = ogData[i][0]
        previousData[i][0] = ogData[i][0]
        currentData[i][1] = ogData[i][1]
        previousData[i][1] = ogData[i][1]
        currentData[i][2] = 2
    i = i + 1
    
    
endCondition = False
while(endCondition == False):
    i = 0
    sum1x = 0
    sum1y = 0
    sum2x = 0
    sum2y = 0
    counter1 = 0
    counter2 = 0
    distance1 = 0
    distance2 = 0
    j = 0
    while(i < rows):
        if(currentData[i][2] == 1):
            counter1 = counter1 + 1
            sum1x = sum1x + currentData[i][0]
            sum1y = sum1y + currentData[i][1]
        else:
            counter2 = counter2 + 1
            sum2x = sum2x + currentData[i][0]
            sum2y = sum2y + currentData[i][1]
        i = i + 1
    previousData = arrayCopy(currentData,previousData,rows)
    centroids[0][0] = sum1x / counter1
    centroids[0][1] = sum1y / counter1
    centroids[1][0] = sum2x / counter2
    centroids[1][1] = sum2y / counter2
    while(j < rows):
        distance1 = euclid_distance(centroids[0][0],centroids[0][1],currentData[j][0],currentData[j][1])
        distance2 = euclid_distance(centroids[1][0],centroids[1][1],currentData[j][0],currentData[j][1])
        if(distance1 < distance2):
            currentData[j][2] = 1
        else:
            currentData[j][2] = 2
        j = j + 1
        endCondition = checkEndState(currentData,previousData,rows)

i = 1
print()
while(i < rows2 + 1):
    print(" Final Centroid" +str(i) + ": ")
    i = i + 1
    j = 0
    while(j < cols):
        print("x" + str(j + 1) +": " + str(centroids[i-2][j]) + " "  )
        j = j + 1

cost = 0
i = 0
distance = 0
plot2 = plot.figure(2)
while(i < rows):
    if(currentData[i][2] == 1):
        distance = euclid_distance(currentData[i][0],currentData[i][1],centroids[0][0],centroids[0][1])
        distance = distance * distance
        cost = cost + distance
        plot.scatter(currentData[i][0],currentData[i][1],color = "red",marker = "o")
    else:
        distance = euclid_distance(currentData[i][0],currentData[i][1],centroids[1][0],centroids[1][1])
        distance = distance * distance
        cost = cost + distance
        plot.scatter(currentData[i][0],currentData[i][1],color = "green",marker = "o")
    i = i + 1   
cost = cost / rows
print("\nError is " + str(cost))

plot.xlabel("x1 Axis")
plot.ylabel("x2 Axis")
plot.title("Clustered Data Points")
plot.savefig("Clustered_Data_Points.png",bbox_inches = "tight")
plot.show()
