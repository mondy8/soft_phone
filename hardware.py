import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
 
# GPIO18ピンの入力状態を表示する
print GPIO.input(18)
 
# GPIOピンをリセット
GPIO.cleanup()