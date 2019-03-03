import socket
import threading
import time
import RPi.GPIO as GPIO

### Server Setting ###
HOSTNAME = "10.0.1.44"
PORT = 12345
CLIENTNUM = 2

class ConnClient(threading.Thread):

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.conn_socket = conn
        self.addr = addr

       

    def run(self):
        try: 
            ### Hardware Setting ###
            valve = 8
            motor_inp1 = 10 #motor input1 右回り
            motor_inp2 = 12 #motor input1 左回り
            pressure = 16 #圧力センサ
            enA = 18 #motor enableA
            mode = 1 #電話の状態
            air_in = 90 #空気の入れ具合(最大100)
            mode = 1
            mode01_condition = 1
            partner_sqz = 0
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(valve, GPIO.OUT)
            GPIO.setup(motor_inp1, GPIO.OUT)
            GPIO.setup(motor_inp2, GPIO.OUT)
            GPIO.setup(enA, GPIO.OUT)
            GPIO.setup(pressure, GPIO.IN)
            GPIO.output(motor_inp1, 1)
            GPIO.output(motor_inp2, 0)
            enA_pwm = GPIO.PWM(enA, 1000)
            enA_pwm.start(0)
            recvdata = 0

            while (1):

                # senddata = input(str(self.addr)+" SendData:")
                # self.conn_socket.send(senddata.encode())
                # recvdata = self.conn_socket.recv(1024) 
                # print("ReciveData:"+str(recvdata))
                # if (recvdata == "quit") or (senddata == "quit"):
                #     break
                
                ####圧力確認
                value = GPIO.input(pressure)
                # GPIO18ピンの入力状態を表示する
                print("input:"+str(value)+",mode:"+str(mode)+",opponentData:"+str(recvdata))
                time.sleep(0.1)
                if recvdata == 1:
                    mode = 3

                if mode == 1: #何もしていない

                    if mode01_condition == 1: #空気を補填中
                        if value == 0:
                            enA_pwm.ChangeDutyCycle(air_in)
                            GPIO.output(valve, 0) #空気ためる
                            senddata = "0"
                        elif value == 1:
                            enA_pwm.ChangeDutyCycle(0)
                            GPIO.output(valve, 1) #空気ぬける
                            time.sleep(0.1)
                            mode01_condition = 2
                            senddata = "0"

                    elif mode01_condition == 2: #空気を補填済み
                        enA_pwm.ChangeDutyCycle(0)
                        GPIO.output(valve, 0) #空気ためる
                        if value == 1: #にぎった
                            mode = 2
                            senddata = "1" #にぎったときsendataを1にする
                        elif value == 0:
                            senddata = "0"

                elif mode == 2: #にぎっている

                    if value == 1: #にぎっている
                        enA_pwm.ChangeDutyCycle(0)
                        GPIO.output(valve, 0) #空気ためる
                        senddata = "1" #にぎったときsendataを1にする
                    elif value == 0: #手を離した
                        mode = 1
                        mode01_condition = 1
                        senddata = "0"

                elif mode == 3: #にぎられている
                    if partner_sqz == 1:
                        if value == 0:
                            enA_pwm.ChangeDutyCycle(air_in)
                            GPIO.output(valve, 0) #空気ためる                            
                            senddata = "0"
                        elif value == 1:
                            enA_pwm.ChangeDutyCycle(0)
                            GPIO.output(valve, 0) #空気ためる
                            senddata = "0"
                    elif partner_sqz == 0:
                        mode = 1
                        mode01_condition = 1
                        senddata = "0"

                """
                
                if [センサーの条件]:
                    self.conn_socket.send(b"1234567")

                recvdata = self.conn_socket.recv(1024) 
                if recvdata:
                    [膨らませる処理]

                """
                self.conn_socket.send(senddata.encode())
                recvdata = self.conn_socket.recv(1024) 


        except socket.error:
            print("connect error")
  
        finally:
            enA_pwm.stop()
            GPIO.cleanup()
            self.conn_socket.close()
            print("connect close")

    def stop(self):
        self.conn_socket.close()

def main():
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s_socket.bind((HOSTNAME, PORT))
        s_socket.listen(CLIENTNUM)
    
        while (1):
            conn, addr = s_socket.accept()
            print("Conneted by"+str(addr))
            connClientThread = ConnClient(conn,addr)
            connClientThread.setDaemon(True)
            connClientThread.start()    

if __name__ == '__main__':
    main()