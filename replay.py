import pickle as pkl
import time
import sys
import os

filename = input("Enter name of file: ")
file = open("replays/" + filename, 'rb')
printStrings = pkl.load(file)
file.close()

for i in range(len(printStrings)):
    str = ""
    height, width = printStrings[0].shape
    for j in range(height):
        for k in range(width):
            str += printStrings[i][j][k]
        str += '\n'
    str += '\0'
    sys.stdout.write(str)
    print('\033[0;0H')
    time.sleep(1/30)
    
        