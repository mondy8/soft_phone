import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN)

while(1):
    value = GPIO.input(18)
    # GPIO18ピンの入力状態を表示する
    print("input:"+str(value))

# GPIOピンをリセット
# GPIO.cleanup()