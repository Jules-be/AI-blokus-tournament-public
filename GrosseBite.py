import fileinput
import sys

def getmap():
    print("BOARD")
    for line in fileinput.input():
        pass
    line.rstrip()
    return line

def checkPiece(x):
    print("PIECE ", x)
    for line in fileinput.input():
        pass
    line.rstrip()
    if (line == "ALREADY PLACED\nDONE\n"):
        return 84
    else:
        return 0