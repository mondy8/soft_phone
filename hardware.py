import time
import RPi.GPIO as GPIO

valve = 8
motor_inp1 = 10 #motor input1 右回り
motor_inp2 = 12 #motor input1 左回り
pressure = 16 #圧力センサ
enA = 18 #motor enableA

GPIO.setmode(GPIO.BOARD)
GPIO.setup(valve, GPIO.OUT)
GPIO.setup(motor_inp1, GPIO.OUT)
GPIO.setup(motor_inp2, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(pressure, GPIO.IN)

while(1):
    ####圧力確認
    value = GPIO.input(pressure)
    # GPIO18ピンの入力状態を表示する
    print("input:"+str(value))
    time.sleep(0.1)

    ####モーター駆動
    GPIO.output(motor_inp1, 1)
    GPIO.output(motor_inp2, 0)
    # PWM/100Hzに設定
    MOTOR_LEVEL = GPIO.PWM(enA, 80)
    # 初期化
    MOTOR_LEVEL.start(0)

    ####valve
    if value == 0 :
        GPIO.output(valve, 0)
    elif value == 1 :
        GPIO.output(valve, 1)


# GPIOピンをリセット
# GPIO.cleanup()