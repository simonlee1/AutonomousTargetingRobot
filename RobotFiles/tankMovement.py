# import curses and GPIO
#import curses
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)

# Motor 2 = left motor

motor1a = 4
motor1b = 17
motor1e = 25

motor2a = 27
motor2b = 23
motor2e = 22

actMotor1 = 21
actMotor2 = 20 
acte = 16

GPIO.setup(motor1a,GPIO.OUT)
GPIO.setup(motor1b,GPIO.OUT)
GPIO.setup(motor1e,GPIO.OUT)
GPIO.setup(motor2a,GPIO.OUT)
GPIO.setup(motor2b,GPIO.OUT)
GPIO.setup(motor2e,GPIO.OUT)
GPIO.setup(actMotor1, GPIO.OUT)
GPIO.setup(actMotor2, GPIO.OUT)
GPIO.setup(acte, GPIO.OUT)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys

def lowerArm(time):
    GPIO.output(acte, GPIO.HIGH)
    GPIO.output(actMotor1, GPIO.HIGH)
    GPIO.output(actMotor2, GPIO.LOW)
    sleep(time)
    stop()

def raiseArm(time):
    GPIO.output(acte, GPIO.HIGH)
    GPIO.output(actMotor1, GPIO.LOW)
    GPIO.output(actMotor2, GPIO.HIGH)
    sleep(time)
    stop()

def stop():
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor1e,GPIO.LOW)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.LOW)
    GPIO.output(motor2e,GPIO.LOW)
    GPIO.output(actMotor1, GPIO.LOW)
    GPIO.output(actMotor2, GPIO.LOW)
    GPIO.output(acte, GPIO.LOW)

def moveForward(time):
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.HIGH)
    GPIO.output(motor1e,GPIO.HIGH)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.HIGH)
    GPIO.output(motor2e,GPIO.HIGH)
    
    sleep(time)
    
    stop()

def motorAF(time):
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.HIGH)
    GPIO.output(motor2e,GPIO.HIGH)
    
    sleep(time)
    
    stop()
    
def motorAB(time):
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPIO.LOW)
    GPIO.output(motor2e,GPIO.HIGH)
    
    sleep(time)
    
    stop()
    
def moveBack(time):
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor1e,GPIO.HIGH)
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPIO.LOW)
    GPIO.output(motor2e,GPIO.HIGH)
    
    sleep(time)
    
    stop()
    
def turnRight(time):
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.HIGH)
    GPIO.output(motor2e,GPIO.HIGH)
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor1e,GPIO.HIGH)
    
    sleep(time)
    
    stop()
    
def turnLeft(time):
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.HIGH)
    GPIO.output(motor1e,GPIO.HIGH)
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPIO.LOW)
    GPIO.output(motor2e,GPIO.HIGH)
    
    sleep(time)
    
    stop()

def cleanUp():
    #curses.nocbreak(); screen.keypad(0); curses.echo()
    #curses.endwin()
    GPIO.cleanup()
    
### 90 degree turn = 0.375
    
if __name__ == "__main__":
    try:
        
        moveForward(10)
        '''
        sleep(1)
        turnRight(0.15) #turnRight(0.375)
        sleep(1)
        turnRight(0.10)
        sleep(1)
        moveForward(4)
        sleep(1)
        turnLeft(.1)
        sleep(.5)
        turnLeft(0.05)
        sleep(1)
        moveForward(3)
        sleep(1)
        turnRight(0.1)
        sleep(0.25)
        turnRight(0.15)
        sleep(.5)
        moveForward(2)
        sleep(1)
        turnRight(0.10)
        sleep(.25)
        turnRight(0.15)
        sleep(1)
        moveForward(1)
        sleep(.1)
        moveForward(0.5)
        sleep(.1)
        moveForward(0.1)
        sleep(.1)
        turnRight(.75)
        raiseArm(15)
        sleep(5)
        lowerArm(15)
        
        moveForward(5)
        sleep(1)
        turnRight(0.25) #turnRight(0.375)
        sleep(1)
        turnRight(0.05)
        sleep(1)
        moveForward(3)
        sleep(1)
        turnLeft(.2)
        sleep(.5)
        turnLeft(0.15)
        sleep(1)
        moveForward(4)
        sleep(1)
        turnRight(0.1)
        sleep(0.25)
        turnRight(0.15)
        sleep(.5)
        moveForward(2)
        sleep(1)
        turnRight(0.10)
        sleep(.25)
        turnRight(0.15)
        sleep(1)
        moveForward(1)
        sleep(.1)
        moveForward(0.5)
        sleep(.1)
        moveForward(0.1)
        sleep(.1)
        turnRight(.4)
        raiseArm(15)
        sleep(5)
        lowerArm(15)
        '''
        
        cleanUp()
    except Exception as e:
        print(e)
        stop()
        pass
