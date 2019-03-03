import time
import RPi.GPIO as GPIO

valve = 8
motor_inp1 = 10 #motor input1 右回り
motor_inp2 = 12 #motor input1 左回り
pressure = 16 #圧力センサ
enA = 18 #motor enableA
mode = 1 #電話の状態

GPIO.setmode(GPIO.BOARD)
GPIO.setup(valve, GPIO.OUT)
GPIO.setup(motor_inp1, GPIO.OUT)
GPIO.setup(motor_inp2, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(pressure, GPIO.IN)

try:  
    ####モーター駆動
    GPIO.output(motor_inp1, 1)
    GPIO.output(motor_inp2, 0)
    # PWM/100Hzに設定
    enA_pwm = GPIO.PWM(enA, 1000)
    # 初期化
    enA_pwm.start(0)
    mode = 1
    mode01_condition = 1

    while(1):

        ####圧力確認
        value = GPIO.input(pressure)
        # GPIO18ピンの入力状態を表示する
        print("input:"+str(value))
        time.sleep(0.1)
        
        
        if mode == 1: #何もしていない

            if mode01_condition == 1: #空気を補填中
                if value == 0:
                    enA_pwm.ChangeDutyCycle(90)
                    GPIO.output(valve, 0) #空気ためる
                elif value == 1:
                    enA_pwm.ChangeDutyCycle(0)
                    GPIO.output(valve, 1) #空気ぬける
                    time.sleep(0.5)
                    mode01_condition = 2

            elif mode01_condition == 2: #空気を補填済み
                    enA_pwm.ChangeDutyCycle(0)
                    GPIO.output(valve, 0) #空気ためる
                    if value == 1: #にぎった
                        mode = 2

        elif mode == 2: #にぎっている

            if value == 1: #にぎっている
                enA_pwm.ChangeDutyCycle(0)
                GPIO.output(valve, 0) #空気ためる
            elif value == 0: #手を離した
                mode = 1
                mode01_condition = 1

        elif mode == 3: #にぎられている
            enA_pwm.ChangeDutyCycle(0)
            GPIO.output(valve, 0) #空気ためる


except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print ("Keyboard Interrupted!")  
  
# except:  
#     # this catches ALL other exceptions including errors.  
#     # You won't get any error messages for debugging  
#     # so only use it once your code is working  
#     print ("Other error or exception occurred!")  
  
finally:  
    enA_pwm.stop()
    GPIO.cleanup() # this ensures a clean exit  

