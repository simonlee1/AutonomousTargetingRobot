import accel
import gps
import tankMovement
import serverSocket
import threading
import math
from time import sleep
import matplotlib.pyplot as plt

tankMovement.stop()

data = {"coordinates": [],
        "initData": [],
        "receivedData":"false",
        "numberHits": 0,
        "done": False,
        "detectHit": False
        }

def runServer():
    serverSocket.make_app(data)

def hitHelper():
    while data["detectHit"]:
        try:
            if accel.getHit()[2] > 3:
                data["numberHits"] += 1
                sleep(0.3)
        except Exception as e:
            print(e)
            


def getHits():
    hits = threading.Thread(target=hitHelper)
    print("start now")
    data["detectHit"] = True
    hits.start()
    sleep(5)
    data["detectHit"] = False


def adjustDir(curLoc, nextLoc):
    toGoDirection = math.atan2(nextLoc[0]-curLoc[0],nextLoc[1]- curLoc[1]) * (180.0/math.pi)


    if nextLoc[0] > curLoc[0]:
        if nextLoc[1] > curLoc[1]:
            #print(1)
            #print(toGoDirection)
            toGoDirection = 90 - toGoDirection
        else:
            #print(2)
            #print(toGoDirection)
            toGoDirection = math.atan2(curLoc[0]- nextLoc[0],curLoc[1]-nextLoc[1]) * (180.0/math.pi)
            toGoDirection = 270 + abs(toGoDirection)
    else:
        if nextLoc[1] > curLoc[1]:
            #print(3)
            #print(toGoDirection)
            toGoDirection = 90 + abs(toGoDirection)
        else:
            #print(4)
            #print(toGoDirection)
            toGoDirection = 90 + abs(toGoDirection)
    #print('trying to go:', toGoDirection)

    while True:
        while True:	
            try:
                curDirection = accel.getDirection()
                break
            except:
            	pass

        otherDirection = 0
        #print("curLocation:",curDirection)
        #print("togo:", toGoDirection)
        if curDirection >= 180:
            otherDirection = curDirection - 180
        else:
            otherDirection = curDirection + 180

        #print(curDirection)

        error = abs(curDirection - toGoDirection)
        #print("error:", error)

        margin = 5
        p = 0.002


        if error < margin :
            break
        #print(error)

        if curDirection > 180:
            if toGoDirection > otherDirection and toGoDirection < curDirection:
                tankMovement.turnLeft(p* error)
            else:
                tankMovement.turnRight(p* error)
        else:
            if toGoDirection > curDirection and toGoDirection < otherDirection:
                tankMovement.turnRight(p* error)
            else:
                tankMovement.turnLeft(p*error)


        sleep(0.5)


#         #tankMovement.stop()

def main():
    x = threading.Thread(target=runServer)
    x.start()
    p = 30000
    samples = 10

    curLoc = getMean(gps.getLoc(samples))
    origLoc = curLoc
    data["coordinates"].append(curLoc)
    #print(data["coordinates"])

    while data["receivedData"] == "false":
        print("waiting for Coordinates")
        sleep(1)
    #nextLoc = [0,1]
    #nextLoc[0] = curLoc[0]+ 0.0000049831 * 4 #0.11132
    #nextLoc[1] = curLoc[1]+ 0.0000049831* 4
    print(data["initData"])

    points = [[x[1:-1].split("^")[0], x[1:-1].split("^")[1]] for x in data["initData"].split(",")[:-1]]
    #points = [["33.643245", "-117.823145"], ["33.648425", "-117.832463"], ["33.639473", "-117.819472"]]

    for point in points:
        nextLoc = point
        if "(" in nextLoc[0]:
            nextLoc[0] = nextLoc[0].replace("(", "")
        if "(" in nextLoc[1]:
            nextLoc[1] = nextLoc[1].replace("(", "")
        nextLoc[0] = float(nextLoc[0])
        nextLoc[1] = float(nextLoc[1])
        print("Were going")
        while True:

            #nextLoc = (curLoc[0] + 0.11132, curLoc[1])
            # print("LatError:", abs(curLoc[0] - nextLoc[0]))
            # print("LongError:", abs(curLoc[1] - nextLoc[1]))
            curLoc = getMean(gps.getLoc(samples))
            data["coordinates"].insert(0,curLoc)
            if abs(curLoc[0] - nextLoc[0]) <= 0.000035 and abs(curLoc[1] - nextLoc[1]) <= 0.000035:
                break
            print(abs(curLoc[0] - nextLoc[0]), abs(curLoc[1] - nextLoc[1]))
            adjustDir(curLoc, nextLoc)


            tankMovement.moveForward(p* math.sqrt((curLoc[0] - nextLoc[0])**2+ (curLoc[1] - nextLoc[1])**2))
        print("we there")
        adjustDir(curLoc, origLoc)
        tankMovement.raiseArm(7)
        getHits()
        tankMovement.lowerArm(9)
        #hitting stuffs


    nextLoc = origLoc
    while True:

        #nextLoc = (curLoc[0] + 0.11132, curLoc[1])
        # print("LatError:", abs(curLoc[0] - nextLoc[0]))
        # print("LongError:", abs(curLoc[1] - nextLoc[1]))
        if abs(curLoc[0] - nextLoc[0]) <= 0.000035 and abs(curLoc[1] - nextLoc[1]) <= 0.000035:
            break
        print(abs(curLoc[0] - nextLoc[0]), abs(curLoc[1] - nextLoc[1]))
        adjustDir(curLoc, nextLoc)
        curLoc = getMean(gps.getLoc(samples))

        tankMovement.moveForward(p* math.sqrt((curLoc[0] - nextLoc[0])**2+ (curLoc[1] - nextLoc[1])**2))

    data["done"] = True
    print("we done")
    quit()
    #adjustDir(curLoc, nextLoc)

    # nextLoc[0] = curLoc[0] - 1.73205 #0.11132
    # nextLoc[1] = curLoc[1] - 1
    # adjustDir(curLoc, nextLoc)
    # print("Should be: 360")
    # print()

    # nextLoc[0] = curLoc[0] #0.11132
    # nextLoc[1] = curLoc[1] - 0.0000089831* 5
    # adjustDir(curLoc, nextLoc)
    # print("Should be: 270")
    # print()

    # nextLoc[0] = curLoc[0]- 0.0000089831 * 5 #0.11132
    # nextLoc[1] = curLoc[1]
    # adjustDir(curLoc, nextLoc)
    # print("Should be: 180")
    # print()

    # nextLoc[0] = curLoc[0] #0.11132
    # nextLoc[1] = curLoc[1]+ 0.0000089831* 5
    # adjustDir(curLoc, nextLoc)
    # print("Should be: 90")
    # print()

    # nextLoc[0] = curLoc[0]+ 0.0000089831 * 5 #0.11132
    # nextLoc[1] = curLoc[1]+ 0.0000089831 * 5
    # adjustDir(curLoc, nextLoc)
    # print("Should be: 45")
    # print()

    # nextLoc[0] = curLoc[0] + 0.0000089831 * 5#0.11132
    # nextLoc[1] = curLoc[1]- 0.0000089831* 5
    # adjustDir(curLoc, nextLoc)
    # print("Should be: 315")
    # print()

    # nextLoc[0] = curLoc[0]- 0.0000089831 * 5 #0.11132
    # nextLoc[1] = curLoc[1]+ 0.0000089831 * 5
    # adjustDir(curLoc, nextLoc)
    # print("Should be: 135")
    # print()

    # nextLoc[0] = curLoc[0]- 0.0000089831 * 5  #0.11132
    # nextLoc[1] = curLoc[1]- 0.0000089831 * 5
    # adjustDir(curLoc, nextLoc)
    # print("Should be: 225")
    # print()

def pltGraph():
    data = gps.getLoc(60)
    y1 = [x[0] for x in data]
    y2 = [x[1] for x in data]
    x1 = range(60)

    fig, axs  = plt.subplots(2)
    axs[0].plot(x1,y1, label = "lat")

    axs[1].plot(x1,y2, label = "long")

    plt.show()

def getMean(gpsCoord):
    lat = sum([x[0] for x in gpsCoord])/len(gpsCoord)
    lon = sum([x[1] for x in gpsCoord])/len(gpsCoord)
    return [lat,lon]

def calibrate():
    while True:
        try:
            print(accel.getDirection())
        except:
            pass


if __name__ == "__main__":
    #main()
    #print(getMean(gps.getLoc(10)))
    #tankMovement.raiseArm(15)
    #getHits()
    #print(data["numberHits"])
    # data["receivedData"] = True
    # #()
    # #calibrate()
    # print("Server started")
    # runServer()
    #calibrate()
    x = threading.Thread(target=runServer)
    x.start()

    # #runServer()
    curLoc = [1,2]
    origLoc = curLoc
    data["coordinates"].append(curLoc)
    #print(data["coordinates"])

    while data["receivedData"] == "false":
        print("waiting for Coordinates")
        sleep(1)

    #print(data)

    #calibrate()
    tankMovement.raiseArm(7)
    getHits()
    tankMovement.lowerArm(9)
    data["done"] = True
   	#main()


    