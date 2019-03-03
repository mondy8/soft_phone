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

try:  
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
        enA_pwm = GPIO.PWM(enA, 1000)
        # 初期化
        enA_pwm.start(80)

        ####valve
        if value == 0 :
            GPIO.output(valve, 0)
        elif value == 1 :
            GPIO.output(valve, 1)

except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print ("Keyboard Interrupted!")  
  
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print ("Other error or exception occurred!")  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit  

