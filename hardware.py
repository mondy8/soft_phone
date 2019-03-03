import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(18, GPIO.IN)

while(1):
    value = GPIO.input(18)
    # GPIO18ピンの入力状態を表示する
    print("input:"+str(value))
    time.sleep(0.1)

    if value == 0 :
        GPIO.output(8, 0)
    elif value == 1 :
        GPIO.output(8, 1)


# GPIOピンをリセット
# GPIO.cleanup()