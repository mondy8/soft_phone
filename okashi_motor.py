import time
import RPi.GPIO as GPIO
import atexit

vibrate_time = 2


class OkashiMotor:

    pinNo = [(8, 10, 12), (33, 35, 37), (16, 18, 32)]

    def __init__(self):

        print("motor")
        print(self.pinNo[0][0])
        print(self.pinNo[1][0])
        self.setting()

    def setting(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        # right
        GPIO.setup(self.pinNo[0][0], GPIO.OUT)
        GPIO.setup(self.pinNo[0][1], GPIO.OUT)
        GPIO.setup(self.pinNo[0][2], GPIO.OUT)
        # center
        GPIO.setup(self.pinNo[1][0], GPIO.OUT)
        GPIO.setup(self.pinNo[1][1], GPIO.OUT)
        GPIO.setup(self.pinNo[1][2], GPIO.OUT)
        # left
        GPIO.setup(self.pinNo[2][0], GPIO.OUT)
        GPIO.setup(self.pinNo[2][1], GPIO.OUT)
        GPIO.setup(self.pinNo[2][2], GPIO.OUT)

        self.pwmR = GPIO.PWM(self.pinNo[0][2], 50)
        
        self.pwmC = GPIO.PWM(self.pinNo[1][2], 50)
        
        self.pwmL = GPIO.PWM(self.pinNo[2][2], 50)
        
    def terminate(self):
        GPIO.cleanup()


#######################

    def cycleMotor(self, id):
        
        if(id == "R"):
            print("motor R")
            self.cycleMotorRight()
        elif(id == "C"):
            print("motor C")
            self.cycleMotorCenter()
        elif(id == "L"):
            print("motor L")
            self.cycleMotorLeft()

    def cycleMotorRight(self):
        self.pwmR.start(0)
        self.pwmR.ChangeDutyCycle(0)
        GPIO.output(self.pinNo[0][0], 0)
        GPIO.output(self.pinNo[0][1], 1)

        self.pwmR.ChangeDutyCycle(100)
        time.sleep(vibrate_time)

        print("stop")

        GPIO.output(self.pinNo[0][0], 0)
        GPIO.output(self.pinNo[0][1], 0)
        time.sleep(2)

        self.pwmR.stop()

    def cycleMotorCenter(self):
        self.pwmC.start(0)
        self.pwmC.ChangeDutyCycle(0)
        GPIO.output(self.pinNo[1][0], 0)
        GPIO.output(self.pinNo[1][1], 1)

        self.pwmC.ChangeDutyCycle(100)
        time.sleep(vibrate_time)

        print("stop")

        GPIO.output(self.pinNo[1][0], 0)
        GPIO.output(self.pinNo[1][1], 0)
        time.sleep(2)

        self.pwmC.stop()

    def cycleMotorLeft(self):
        self.pwmL.start(0)
        self.pwmL.ChangeDutyCycle(0)
        GPIO.output(self.pinNo[2][0], 0)
        GPIO.output(self.pinNo[2][1], 1)

        self.pwmL.ChangeDutyCycle(100)
        time.sleep(vibrate_time*2)

        print("stop")

        GPIO.output(self.pinNo[2][0], 0)
        GPIO.output(self.pinNo[2][1], 0)
        time.sleep(2)

        self.pwmL.stop()


if __name__ == "__main__":
    om = OkashiMotor()
    atexit.register(om.terminate)
    om.cycleMotor("R")
    om.cycleMotor("C")
    om.cycleMotor("L")
    om.cycleMotor("R")
    om.cycleMotor("C")
    om.cycleMotor("L")

