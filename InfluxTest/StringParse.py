## this script will parse an input and save the values of the string as elements in an array
# Influx imports
import numpy as np
import matplotlib.pyplot as plt




def parseString(inputString):
    dataArray = np.empty((50, 2))
    count = 0    
    dataPoints = inputString.split(",",2)
    pointsString = dataPoints[2].replace(",", "") 
    epochTime = float(dataPoints[1])
    pointsString = pointsString.strip(" ")
    stringArray = pointsString.split(" ")
        
    for a in stringArray:
        
        dataArray[count][1] = float(a)
        dataArray[count][0] = epochTime
        epochTime+=.005
        count+=1  
    return dataArray



parseString("'SHZ', 1507760140.530, 614, 916, 1095, 1156, 839, 923, 861, 856, 861, 789, 568, 823, 965, 788, 835, 991, 1028, 1225, 1142, 828, 682, 635, 771, 978, 834, 1167, 1116, 888, 627, 564, 944, 994, 780, 652, 811, 915, 832, 1134, 1020, 594, 756, 782, 748, 810, 864, 936, 977, 1014, 676, 502")