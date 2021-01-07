import board
import busio
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import math
import digitalio
import adafruit_lis3dh

i2c = busio.I2C(board.SCL, board.SDA)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

other = busio.I2C(board.SCL, board.SDA)
#int1 = digitalio.DigitalInOut(13)
hit = adafruit_lis3dh.LIS3DH_I2C(other)


def getAccel():
    return accel.acceleration

def getHit():
    return hit.acceleration

def getDirection():
    data = mag.magnetic
    xVal = data[0] + 10
    yVal = data[1] + 25
    
    #return math.atan2(yVal,xVal) * (180.0/math.pi)
    
    
    if xVal == 0:
        if yVal >= 0:
            D = 0 
        else:
            D = 90
    else:
        #if xVal >0:
            #D = math.atan(yVal/xVal) * (180.0/math.pi)
        #else:
        D = math.atan2(yVal,xVal) * (180.0/math.pi)
        
    if D > 360:
        return D - 360
    elif D < 0:
        return D + 360
    else:
        return D
    
    
    
if __name__ == "__main__":
    while True:
        for i in range(10000000):
            print(getDirection())