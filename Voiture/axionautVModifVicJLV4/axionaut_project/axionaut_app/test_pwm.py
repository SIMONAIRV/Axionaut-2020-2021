import Adafruit_PCA9685
import time

servo = Adafruit_PCA9685.PCA9685()
servo.set_pwm_freq(50)

while True: 
    servo.set_pwm(0,0,205)
    time.sleep(1)
    servo.set_pwm(0,0,307)
    time.sleep(1)
    servo.set_pwm(0,0,410)
    time.sleep(1)
    servo.set_pwm(0,0,307)
    time.sleep(1)